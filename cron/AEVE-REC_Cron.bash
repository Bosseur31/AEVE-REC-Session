#!/bin/bash


#Dossier de base
dir=/srv/aeve-rec-session/data/temp ;
dir_timestamp=/srv/aeve-rec-session/back/temp_var ;
filename="$dir_timestamp/timestamp.txt" ;
date_log=$(date '+%d/%m/%Y %r') ;

#Time for save temp video
timestamp_save=$((2595600))


if [ ! -f $filename ]
then
    touch $filename
fi

#Récupération du dernier timestamp de transfer

timestamp_modif=$(cat "$filename") ;

if [ "$timestamp_modif" == '' ]
then
    echo "1577833200" > "$filename" ;
    timestamp_modif=$(cat "$filename") ;
fi

#Ecriture du timestamp 
timestamp_final=$(date +%s) ;
echo "$timestamp_final" > "$filename" ;

echo '------------------------------------'
echo '------------------------------------'
echo '------------------------------------'
echo '---- Nouvelle synchronisation ! ----'
echo '------------------------------------'
echo '------------------------------------'
echo 'Date :' $date_log
echo '------------------------------------'
echo '------------------------------------'
echo "Dernier transfer: "$timestamp_modif
echo '------------------------------------'
echo '------------------------------------'
echo '------------------------------------'

for video in $dir/*
do
   #Nom du fichier apres son répertoire
   destVideo=$(basename "$video");
   #Nom du répertoire
   srcVideo=$(dirname $video);

   #Récupération du timestamp de dérniere modif de la vidéo
   timestamp=$(stat -c '%Y' "$dir/$destVideo") ;

   if [ "$timestamp" -lt "$timestamp_modif" ] 
   then
      echo "Vidéo deja traité :" $video

      continue
   fi



   if [ "$timestamp" -lt "$timestamp_modif - $timestamp_save" ]
   then
      echo "Video a plus de 30 jours :" $video
   fi

   jour=$(date -d @"$(echo $timestamp)" +'%Y-%m-%d') ;
   mois=$(date -d @"$(echo $timestamp)" +'%m.%y') ;
   semaine=$(date --date=$jour +"%V") ;
   annee=$(date -d @"$(echo $timestamp)" +'%Y')
   
   #Remplacement des espaces pour URL
   echo "$destVideo"|sed -e 's/ /%20/g'
   
   #Chemin de la destination et debug
   destnext="https://cloud.aymeric-mai.fr/remote.php/dav/files/simon/Simon/Vidéos-Simon/$(echo "$annee")/Semaine-$semaine%20le%20$mois/$(echo "$destVideo"|sed -e 's/ /%20/g')"
   

   #Execution de la commande de transfert
   log=$(curl -u simon:tchaik01 -T "$video" "https://cloud.aymeric-mai.fr/remote.php/dav/files/simon/Simon/Vidéos-Simon/$(echo "$annee")/Semaine-$semaine%20le%20$mois/$(echo "$destVideo"|sed -e 's/ /%20/g')")
   echo $log
   
   #Debug
   echo "Nom video : "$destVideo
   echo "Timestamp de la derniére modification de la vidéo: "$timestamp
   echo "Chemin complet : "$video
   echo "La semaine : "$semaine
   echo "Le mois annee : "$mois
   echo "L'année: "$annee
   echo "Destination finale : "$destnext

done
