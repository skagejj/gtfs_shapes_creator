<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="it_IT" sourcelanguage="en_US">
<context>
    <name>GtfsShapesCreator</name>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="200" />
        <source>&amp;GTFS Shapes Creator</source>
        <translation>&amp;Creator di Forme GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="169" />
        <source>Create the shapes.txt for your GTFS</source>
        <translation>Crea il file shapes.txt per il tuo GTFS</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidget</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="204" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on files_to_delete.json</source>
        <translation>I file temporanei verranno eliminati solo riavviando QGIS, i loro percorsi sono salvati su files_to_delete.json</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="222" />
        <source>Starting at {datetime.datetime.now().time().replace(microsecond=0)} the real job (..be patient, please)</source>
        <translation>A partire da {datetime.datetime.now().time().replace(microsecond=0)} il vero lavoro (..sii paziente, per favore)</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1750" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on {files_to_delete_next_bus_loading_json}</source>
        <translation>I file temporanei verranno eliminati solo riavviando QGIS, i loro percorsi sono salvati su {files_to_delete_next_bus_loading_json}</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1184" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : GTFS Shapes Creator has started routing..</source>
        <translation>a {datetime.datetime.now().time().replace(microsecond=0)} : GTFS Shapes Creator ha iniziato il routing..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1222" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on the files_to_delete.json</source>
        <translation>I file temporanei verranno eliminati solo riavviando QGIS, i loro percorsi sono salvati su files_to_delete.json</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1326" />
        <source>Something wrong went creating the trips, GO BACK to step 1, remove the buses concerned and try again</source>
        <translation>Qualcosa è andato male nella creazione dei percorsi, TORNA al step 1, rimuovi gli autobus interessati e riprova</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1386" />
        <source>{trip} is missing</source>
        <translation>{trip} è mancante</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1409" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : Integrating the shapes to the GTFS file take much less time</source>
        <translation>a {datetime.datetime.now().time().replace(microsecond=0)} : L'integrazione delle forme nel file GTFS richiede molto meno tempo</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1565" />
        <source>It's DONE! Find your file in {zip_file}, CONGRATULATION!</source>
        <translation>È FATTO! Trova il tuo file in {zip_file}, CONGRATULAZIONI!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1717" />
        <source>you have never run the plugins with the </source>
        <translation>non hai mai eseguito il plugin con</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1739" />
        <source>the </source>
        <translation>il</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidgetBase</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="20" />
        <source>GTFS Shapes Creator</source>
        <translation>Creator di Forme GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="42" />
        <source>Download a GTFS on opendatatransport.swiss</source>
        <translation>Scarica un GTFS da opendatatransport.swiss</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="61" />
        <source>Browse to the GTFS unzipped Folder</source>
        <translation>Sfoglia la cartella GTFS decompressa</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="130" />
        <source>1st step - agencies selection</source>
        <translation>1° step - selezione agenzie</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="148" />
        <source>Update Agencies</source>
        <translation>Aggiorna Agenzie</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="189" />
        <source>Search the agency</source>
        <translation>Cerca l'agenzia</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="214" />
        <source>Load the PT lines for the selected agencies</source>
        <translation>Carica le linee PT per le agenzie selezionate</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="241" />
        <source>2nd step - transports selection</source>
        <translation>2° step - selezione trasporti</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="287" />
        <source>Load the stops and create the roads/rails 
networks for the selected transports</source>
        <translation>Carica le fermate e crea le reti stradali/ferroviarie per i trasporti selezionati</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="301" />
        <source>It will take lot of time, be patient...</source>
        <translation>Ci vorrà molto tempo, sii paziente...</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="314" />
        <source>Remove precedent loaded liens</source>
        <translation>Rimuovi le linee caricate precedentemente</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="328" />
        <source>3rd step - move the off-road stops</source>
        <translation>3° step - sposta le fermate fuori strada</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="365" />
        <source>Zoom on the selected Stop</source>
        <translation>Zoom sulla fermata selezionata</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="381" />
        <source>Create the paths for each trip</source>
        <translation>Crea i percorsi per ogni viaggio</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="395" />
        <source>4th step - correct the transports paths</source>
        <translation>4° step - correggi i percorsi dei trasporti</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="407" />
        <source>Display Trips</source>
        <translation>Visualizza Viaggi</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="440" />
        <source>Create your shapes.txt
and 
the final GTFS .zip file !</source>
        <translation>Crea il tuo shapes.txt e il file GTFS .zip finale!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="455" />
        <source>you like those trips ? .. </source>
        <translation>ti piacciono questi viaggi? ..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="475" />
        <source> PUSH THE BUTTON!</source>
        <translation>PREMI IL PULSANTE!</translation>
    </message>
</context>
</TS>