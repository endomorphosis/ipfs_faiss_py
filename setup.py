from setuptools import setup

setup(
	name='ipfs-faiss',
	version='0.0.1',
	packages=[
		'ipfs_faiss',
        'ipfs_faiss.model_manager',
        'ipfs_faiss.model_manager.ipfs_kit_lib',
		'ipfs_faiss.model_manager.orbitdb_kit_lib',
        'ipfs_faiss.model_manager.ipfs_datasets_lib',
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