#!/bin/sh
arr=(Carson_Palmer Matt_Ryan Joe_Flacco Thad_Lewis Cam_Newton Jay_Cutler Andy_Dalton
    Jason_Campbell Tony_Romo Peyton_Manning Matthew_Stafford Matt_Flynn Matt_Schaub Andrew_Luck 
    Chad_Henne Alex_Smith Ryan_Tannehill Matt_Cassel Tom_Brady Drew_Brees Eli_Manning Geno_Smith
    Matt_McGloin Nick_Foles Ben_Roethlisberger Philip_Rivers Colin_Kaepernick Russell_Wilson
    Kellen_Clemens Mike_Glennon Ryan_Fitzpatrick Kirk_Cousins Sam_Bradford Aaron_Rodgers Terelle_Pryor
	Josh_McCown)
for var in "${arr[@]}"
do	
	echo $var
	python data_collector.py $var
done
