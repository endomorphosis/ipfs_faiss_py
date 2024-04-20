from setuptools import setup

setup(
	name='ipfs-faiss',
	version='0.0.1',
	packages=[
		'ipfs_faiss',
        'ipfs_faiss.ipfs_kit_lib',
	],
	install_requires=[
        'ipfs_datasets@git+https://github.com/endomorphosis/ipfs_datasets.git',
		'datasets',
		'urllib3',
		'requests',
		'boto3',
	]
)