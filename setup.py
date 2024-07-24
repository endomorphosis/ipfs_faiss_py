from setuptools import setup

setup(
	name='ipfs-faiss',
	version='0.0.2',
	packages=[
		'ipfs_faiss',
	],
	install_requires=[
        'ipfs_datasets@git+https://github.com/endomorphosis/ipfs_datasets.git',
		'datasets',
        "ipfs_model_manager@git+https://github.com/endomorphosis/ipfs_model_manager.git",
        "orbitdb_kit@git@git+https://github.com/endomorphosis/orbitdb_kit.git",
		"ipfs_kit@git+https://github.com/endomorphosis/ipfs_kit.git",
		"faiss",
		'urllib3',
		'requests',
		'boto3',
	]
)