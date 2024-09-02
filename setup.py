from setuptools import setup

setup(
	name='ipfs-faiss_py',
	version='0.0.2',
	packages=[
		'ipfs_faiss',
	],
	install_requires=[
        'ipfs_datasets_py',
		'datasets',
        "ipfs_model_manager_py",
        "orbitdb_kit_py",
		"ipfs_kit_py",
		"faiss",
		'urllib3',
		'requests',
		'boto3',
	]
)