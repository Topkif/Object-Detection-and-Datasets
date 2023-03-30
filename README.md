# MSL-Dataset-Labeling
![RCT Logo](https://rct.univ-tln.fr/wp-content/uploads/IMG_0206-1.jpg)

The dataset of robot's images containt 12 classes of object.
Respect this order when creating a deeplabel project:

* robot
* ballon
* but
* poteau
* tag_bleu
* tag_rouge
* robot_rct
* humain
* brassard_rouge
* brassard_bleu
* cible
* valise


## This dataset contains :

* Images set of Robots (Set from [NuBot Dataset](https://github.com/Abbyls/robocup-MSL-dataset) with more images added)
* Images set of Robots and Ball from our robot's omnivision camera
* Images set of Ball (Not MSL)
* Librairies to labelize images and to generate training set using [DeepLabel Tool](https://github.com/jveitchmichaelis/deeplabel)


## Creating a file with all txt labels (for darknet or import)
In powershell admin run : `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
Then run .\script.ps1
