<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1">
<context>
    <name>GtfsShapesCreator</name>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="200" />
        <source>&amp;GTFS Shapes Creator</source>
        <translation>&amp;Créateur de Formes GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="169" />
        <source>Create the shapes.txt for your GTFS</source>
        <translation>Créez le fichier shapes.txt pour votre GTFS</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidget</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="204" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on files_to_delete.json</source>
        <translation>Les fichiers temporaires ne seront supprimés qu'au redémarrage de QGIS, leurs chemins sont enregistrés dans files_to_delete.json</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="222" />
        <source>Starting at {datetime.datetime.now().time().replace(microsecond=0)} the real job (..be patient, please)</source>
        <translation>À partir de {datetime.datetime.now().time().replace(microsecond=0)} le vrai travail (..soyez patient, s'il vous plaît)</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1750" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on {files_to_delete_next_bus_loading_json}</source>
        <translation>Les fichiers temporaires ne seront supprimés qu'au redémarrage de QGIS, leurs chemins sont enregistrés dans {files_to_delete_next_bus_loading_json}</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1184" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : GTFS Shapes Creator has started routing..</source>
        <translation>à {datetime.datetime.now().time().replace(microsecond=0)} : GTFS Shapes Creator a commencé le routage..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1222" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on the files_to_delete.json</source>
        <translation>Les fichiers temporaires ne seront supprimés qu'au redémarrage de QGIS, leurs chemins sont enregistrés dans files_to_delete.json</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1326" />
        <source>Something wrong went creating the trips, GO BACK to step 1, remove the buses concerned and try again</source>
        <translation>Quelque chose s'est mal passé lors de la création des trajets, RETOURNEZ à l'étape 1, supprimez les bus concernés et réessayez</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1386" />
        <source>{trip} is missing</source>
        <translation>{trip} est manquant</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1409" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : Integrating the shapes to the GTFS file take much less time</source>
        <translation>à {datetime.datetime.now().time().replace(microsecond=0)} : L'intégration des formes dans le fichier GTFS prend beaucoup moins de temps</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1565" />
        <source>It's DONE! Find your file in {zip_file}, CONGRATULATION!</source>
        <translation>C'est FAIT! Trouvez votre fichier dans {zip_file}, FÉLICITATIONS!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1717" />
        <source>you have never run the plugins with the </source>
        <translation>vous n'avez jamais exécuté le plugin avec</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1739" />
        <source>the </source>
        <translation>le</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidgetBase</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="20" />
        <source>GTFS Shapes Creator</source>
        <translation>Créateur de Formes GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="42" />
        <source>Download a GTFS on opendatatransport.swiss</source>
        <translation>Téléchargez un GTFS sur opendatatransport.swiss</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="61" />
        <source>Browse to the GTFS unzipped Folder</source>
        <translation>Parcourez le dossier GTFS décompressé</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="130" />
        <source>1st step - agencies selection</source>
        <translation>1ère étape - sélection des agences</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="148" />
        <source>Update Agencies</source>
        <translation>Mettre à jour les Agences</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="189" />
        <source>Search the agency</source>
        <translation>Rechercher l'agence</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="214" />
        <source>Load the PT lines for the selected agencies</source>
        <translation>Chargez les lignes PT pour les agences sélectionnées</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="241" />
        <source>2nd step - transports selection</source>
        <translation>2e étape - sélection des transports</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="287" />
        <source>Load the stops and create the roads/rails 
networks for the selected transports</source>
        <translation>Chargez les arrêts et créez les réseaux routiers/ferroviaires pour les transports sélectionnés</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="301" />
        <source>It will take lot of time, be patient...</source>
        <translation>Cela prendra beaucoup de temps, soyez patient...</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="314" />
        <source>Remove precedent loaded liens</source>
        <translation>Supprimez les lignes chargées précédemment</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="328" />
        <source>3rd step - move the off-road stops</source>
        <translation>3e étape - déplacer les arrêts hors route</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="365" />
        <source>Zoom on the selected Stop</source>
        <translation>Zoom sur l'arrêt sélectionné</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="381" />
        <source>Create the paths for each trip</source>
        <translation>Créez les trajets pour chaque voyage</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="395" />
        <source>4th step - correct the transports paths</source>
        <translation>4e étape - corriger les trajets de transport</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="407" />
        <source>Display Trips</source>
        <translation>Afficher les Trajets</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="440" />
        <source>Create your shapes.txt
and 
the final GTFS .zip file !</source>
        <translation>Créez votre shapes.txt et le fichier GTFS .zip final!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="455" />
        <source>you like those trips ? .. </source>
        <translation>vous aimez ces trajets? ..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="475" />
        <source> PUSH THE BUTTON!</source>
        <translation>APPUYEZ SUR LE BOUTON!</translation>
    </message>
</context>
</TS>