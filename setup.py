from setuptools import setup, Extension
import discordoauth

version = discordoauth.__version__

setup(
  name = 'discordoauth.py',         
  packages = ['discordoauth'],   
  project_urls={
        "Documentation": "https://github.com/Coolo22/discordoauth.py/docs",
        "Issue tracker": "https://github.com/Coolo22/discordoauth.py/issues",
},
  version = version,     
  license='MIT',       
  description = 'Easily using discord webhooks in python - asynchronous and synchronous - documented at https://github.com/Coolo22/discordoauth.py/docs/', 
  long_description=open("README.md").read(),
  long_description_content_type='text/markdown',
  author = 'Coolo2',                   
  author_email = 'itsxcoolo2@gmail.com',      
  url = 'https://github.com/Coolo22/discordoauth.py',   
  download_url = 'https://github.com/Coolo22/discordwebhook.py/raw/master/archive/discordoauth.py-' + version + '.tar.gz',    
  keywords = ['discord', 'oauth2', 'python', 'api', 'asynchronous', 'synchronous', "oauth"],   
  install_requires=['aiohttp', 'nest_asyncio'],
  classifiers=[
    'Development Status :: 5 - Production/Stable', 
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)