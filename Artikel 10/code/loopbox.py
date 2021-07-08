from machine import I2S, Pin, TouchPad
from time import sleep

WAV_FILE = 'sample.wav'
SAMPLE_RATE_IN_HZ = 16000
RECORD_TIME_IN_SECONDS = 5
WAV_SAMPLE_SIZE_IN_BITS = 16
WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
MIC_SAMPLE_BUFFER_SIZE_IN_BYTES = 4096
SAMPLE_BUFFER_SIZE_IN_BYTES = MIC_SAMPLE_BUFFER_SIZE_IN_BYTES // 2
NUM_SAMPLE_BYTES_TO_WRITE = RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES
NUM_CHANNELS = 1
BUTTON_THRESHOLD = 300
MIC_BCK_PIN = Pin(33)
MIC_WS_PIN = Pin(32)
MIC_SDIN_PIN = Pin(14)
SPK_BCK_PIN = Pin(18)
SPK_WS_PIN = Pin(19)
SPK_SDOUT_PIN = Pin(5)

audio_in = I2S(
  I2S.NUM0, 
  bck = MIC_BCK_PIN, ws = MIC_WS_PIN, sdin = MIC_SDIN_PIN,
  standard = I2S.PHILIPS, 
  mode = I2S.MASTER_RX,
  dataformat = I2S.B32,
  channelformat = I2S.ONLY_LEFT,
  samplerate = SAMPLE_RATE_IN_HZ,
  dmacount = 50,
  dmalen = 256
)

audio_out = I2S(
  I2S.NUM1,
  bck = SPK_BCK_PIN, ws = SPK_WS_PIN, sdout = SPK_SDOUT_PIN, 
  standard = I2S.PHILIPS, 
  mode = I2S.MASTER_TX,
  dataformat = I2S.B16, 
  samplerate = SAMPLE_RATE_IN_HZ,
  channelformat = I2S.ONLY_LEFT,
  dmacount = 10, dmalen = 512)

play_button = TouchPad(Pin(12))
rec_button = TouchPad(Pin(13))
led = Pin(2, Pin.OUT)

def play_button_pressed():
  return play_button.read() < BUTTON_THRESHOLD

def rec_button_pressed():
  return rec_button.read() < BUTTON_THRESHOLD

def snip_16_mono(samples_in, samples_out):
  num_samples = len(samples_in) // 4
  for i in range(num_samples):
    samples_out[2 * i] = samples_in[4 * i + 2]
    samples_out[2 * i + 1] = samples_in[4 * i + 3]            
  return num_samples * 2

def create_wav_header(sample_rate, bits_per_sample, num_channels, num_samples):
  datasize = num_samples * num_channels * bits_per_sample // 8
  h = bytes('RIFF', 'ascii')
  h += (datasize + 36).to_bytes(4, 'little')
  h += bytes('WAVE', 'ascii')
  h += bytes('fmt ', 'ascii')
  h += (16).to_bytes(4, 'little')
  h += (1).to_bytes(2, 'little')
  h += (num_channels).to_bytes(2, 'little')
  h += (sample_rate).to_bytes(4, 'little')
  h += (sample_rate * num_channels * bits_per_sample // 8).to_bytes(4, 'little')
  h += (num_channels * bits_per_sample // 8).to_bytes(2, 'little')
  h += (bits_per_sample).to_bytes(2, 'little')
  h += bytes('data', 'ascii')
  h += (datasize).to_bytes(4, 'little')
  return h

def record_sample(filename):
  mic_samples = bytearray(MIC_SAMPLE_BUFFER_SIZE_IN_BYTES)
  mic_samples_mv = memoryview(mic_samples)
  wav_samples = bytearray(SAMPLE_BUFFER_SIZE_IN_BYTES)
  wav_samples_mv = memoryview(wav_samples)

  wav = open(filename, 'wb')
  wav_header = create_wav_header(
    SAMPLE_RATE_IN_HZ, 
    WAV_SAMPLE_SIZE_IN_BITS, 
    NUM_CHANNELS, 
    SAMPLE_RATE_IN_HZ * RECORD_TIME_IN_SECONDS
  )
  wav.write(wav_header)

  sleep(1)
  led.value(1)

  num_sample_bytes_written_to_wav = 0
  while rec_button_pressed() and (num_sample_bytes_written_to_wav < NUM_SAMPLE_BYTES_TO_WRITE):
    num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv, timeout = 0)
    if num_bytes_read_from_mic > 0:
      num_bytes_snipped = snip_16_mono(
        mic_samples_mv[:num_bytes_read_from_mic],
        wav_samples_mv)
      num_bytes_to_write = min(
        num_bytes_snipped,
        NUM_SAMPLE_BYTES_TO_WRITE - num_sample_bytes_written_to_wav)
      num_bytes_written = wav.write(wav_samples_mv[:num_bytes_to_write])
      num_sample_bytes_written_to_wav += num_bytes_written
  wav_header = create_wav_header(
    SAMPLE_RATE_IN_HZ, 
    WAV_SAMPLE_SIZE_IN_BITS, 
    NUM_CHANNELS, 
    num_sample_bytes_written_to_wav // WAV_SAMPLE_SIZE_IN_BYTES
  )
  wav.seek(0)
  wav.write(wav_header)
  wav.close()
  led.value(0)

def play_sample(filename):
  wav_samples = bytearray(1024)
  wav_samples_mv = memoryview(wav_samples)
  wav = open(filename, 'rb')
  wav.seek(44)
  num_written = 0
  num_read = wav.readinto(wav_samples_mv)
  while num_read != 0:
    while num_written < num_read:
      num_written += audio_out.write(wav_samples_mv[num_written:num_read], timeout = 0)
    num_written = 0
    num_read = wav.readinto(wav_samples_mv)
  wav.close()

while True:
  try:
    while play_button_pressed():
      play_sample(WAV_FILE)
    if rec_button_pressed():
      record_sample(WAV_FILE)
  except (KeyboardInterrupt, Exception) as e:
    print('Exception: {} {}'.format(type(e).__name__, e))
    led.value(0)
    break
    
audio_in.deinit()
audio_out.deinit()
