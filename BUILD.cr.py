
import io
import os
import requests
import tarfile
import craftr, {path} from 'craftr'
import cxx from 'craftr/lang/cxx'

source_url = craftr.options['opus.source_url']

if 'opus.source_dir' not in craftr.cache:
  source_dir = craftr.cell().build_directory
  print('Downloading opus source ...')
  with tarfile.open(fileobj=io.BytesIO(requests.get(source_url).content)) as fp:
    fp.extractall(source_dir)
    source_dir = path.join(source_dir, fp.getmembers()[0].name)
  craftr.cache['opus.source_dir'] = source_dir
else:
  source_dir = craftr.cache['opus.source_dir']

platform_defines = []
if os.name == 'nt':
  platform_defines.append('WIN32')

cxx.library(
  name = 'opus',
  srcs = craftr.glob(
    parent = source_dir,
    patterns = [
      'celt/*.c',
      'silk/*.c',
      'silk/float/*.c',
      'src/*.c',
    ],
    excludes = [
      'celt/opus_custom_demo.c',
      'src/opus_compare.c',
      'src/opus_demo.c',
      'src/repacketizer_demo.c',
      'src/test*.c',
    ]),
  includes = [path.join(source_dir, x) for x in [
    'celt',
    'include',
    'silk',
    'silk/float'
  ]],
  defines = ['USE_ALLOCA=1', 'OPUS_BUILD=1', '__SSE__=1'] + platform_defines,
  shared_defines = ['DLL_EXPORT'],
  preferred_linkage = 'shared',
  unity_build = True
)
