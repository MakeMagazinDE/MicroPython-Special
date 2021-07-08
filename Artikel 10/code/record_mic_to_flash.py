from machine import I2S, Pin

RECORD_TIME_IN_SECONDS = 5
SAMPLE_RATE_IN_HZ = 8000
WAV_SAMPLE_SIZE_IN_BITS = 16
WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
MIC_SAMPLE_BUFFER_SIZE_IN_BYTES = 4096
SAMPLE_BUFFER_SIZE_IN_BYTES = MIC_SAMPLE_BUFFER_SIZE_IN_BYTES // 2 # why divide by 2? only using 16-bits of 32-bit samples
NUM_SAMPLE_BYTES_TO_WRITE = RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES
NUM_CHANNELS = 1

BCK_PIN = Pin(33)
WS_PIN = Pin(32)
SDIN_PIN = Pin(14)

audio_in = I2S(
  I2S.NUM0, 
  bck = BCK_PIN, ws = WS_PIN, sdin = SDIN_PIN,
  standard = I2S.PHILIPS, 
  mode = I2S.MASTER_RX,
  dataformat = I2S.B32,
  channelformat = I2S.ONLY_LEFT,
  samplerate = SAMPLE_RATE_IN_HZ,
  dmacount = 50,
  dmalen = 256
)

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

wav = open('sample.wav', 'wb')
wav_header = create_wav_header(
  SAMPLE_RATE_IN_HZ, 
  WAV_SAMPLE_SIZE_IN_BITS, 
  NUM_CHANNELS, 
  SAMPLE_RATE_IN_HZ * RECORD_TIME_IN_SECONDS
)
wav.write(wav_header)

mic_samples = bytearray(MIC_SAMPLE_BUFFER_SIZE_IN_BYTES)
mic_samples_mv = memoryview(mic_samples)
wav_samples = bytearray(SAMPLE_BUFFER_SIZE_IN_BYTES)
wav_samples_mv = memoryview(wav_samples)

print('Aufnahme startet.')
num_sample_bytes_written_to_wav = 0
while num_sample_bytes_written_to_wav < NUM_SAMPLE_BYTES_TO_WRITE:
  try:
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
  except (KeyboardInterrupt, Exception) as e:
    print('Exception: {} {}'.format(type(e).__name__, e))
    break

wav.close()
audio_in.deinit()
print('WAV-Datei enthält %d Sample-Bytes.' % num_sample_bytes_written_to_wav)
