import os, shutil

def copy_static(source, destination, clean=False):
	# delete public directory
	if clean and os.path.exists(destination):
		shutil.rmtree(destination)
	# make new public directory
	if not os.path.exists(destination):
		os.mkdir(destination)
	
	# recurse through src
	for entry in os.listdir(source):
		src_path = os.path.join(source, entry)
		dst_path = os.path.join(destination, entry)
		print(src_path)
		print(dst_path)
		if os.path.isfile(src_path):
			shutil.copy(src_path, dst_path)
		else:
			if not os.path.exists(dst_path):
				os.mkdir(dst_path)
			copy_static(src_path, dst_path, False)