from machine import I2S, Pin, SDCard

WAV_FILE = '/sd/Hallo.wav'
SAMPLE_RATE_IN_HZ = 16000

BCK_PIN = Pin(33)
WS_PIN = Pin(25)
SDOUT_PIN = Pin(32)

audio_out = I2S(
  I2S.NUM0, 
  bck = BCK_PIN, ws = WS_PIN, sdout = SDOUT_PIN, 
  standard = I2S.PHILIPS, 
  mode = I2S.MASTER_TX,
  dataformat = I2S.B16, 
  samplerate = SAMPLE_RATE_IN_HZ,
  channelformat = I2S.ONLY_LEFT,
  dmacount = 10, dmalen = 512)

sd = SDCard(slot = 2, sck = Pin(18), mosi = Pin(23), miso = Pin(19), cs = Pin(5))
uos.mount(sd, '/sd')

wav_samples = bytearray(1024)
wav_samples_mv = memoryview(wav_samples)

wav = open(WAV_FILE, 'rb')
wav.seek(44) 

while True:
  try:
    num_written = 0
    num_read = wav.readinto(wav_samples_mv)
    if num_read == 0: # Ende der WAV-Datei?
      wav.seek(44) # Dann zurück zum Anfang.
    else:
      while num_written < num_read:
        num_written += audio_out.write(wav_samples_mv[num_written:num_read], timeout = 0)
  except (KeyboardInterrupt, Exception) as e:
    print('Exception: {} {}'.format(type(e).__name__, e))
    break
    
wav.close()
audio_out.deinit()
uos.umount('/sd')
sd.deinit()
