Welcome to Tagging Master

Installation requirements:
- install blender 
- use python pip (command 
	python pip -m install -r installationRequirements.txt
			if you install blender in your C director navigate to the install directory, 
				execute pip install with admin rights from this place - it is easier to install blender outside of C firstplace 
				to be able to install with pip directly from blender built in console)
Execution:
- open blender
	- import 3D model
	- import GPX data,  (TODO)
	- manually adapt 3D of model to match route 
	- create cube and position it inside roof and rename it to 'RoofCenter'
	- modify image folder path
	- select route in blender view and execute script generate3DmodelSnapshots.py

- execute Match3D_regeneratedToOriginal.py to find the best generated view from the 3D model

find the best matching screenshot in the Result folder (relative to your image path given above)

open: tags could now be transferred via measuring the distances directly within the two images