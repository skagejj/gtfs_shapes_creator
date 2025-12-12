<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1">
<context>
    <name>GtfsShapesCreator</name>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="200" />
        <source>&amp;GTFS Shapes Creator</source>
        <translation>&amp;Создатель форм GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="169" />
        <source>Create the shapes.txt for your GTFS</source>
        <translation>Создайте файл shapes.txt для вашего GTFS</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidget</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="204" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on files_to_delete.json</source>
        <translation>Временные файлы будут удалены только при перезагрузке QGIS, их пути сохранены в files_to_delete.json</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="222" />
        <source>Starting at {datetime.datetime.now().time().replace(microsecond=0)} the real job (..be patient, please)</source>
        <translation>Начиная с {datetime.datetime.now().time().replace(microsecond=0)} реальная работа (..пожалуйста, будьте терпеливы)</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1750" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on {files_to_delete_next_bus_loading_json}</source>
        <translation>Временные файлы будут удалены только при перезагрузке QGIS, их пути сохранены в {files_to_delete_next_bus_loading_json}</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1184" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : GTFS Shapes Creator has started routing..</source>
        <translation>в {datetime.datetime.now().time().replace(microsecond=0)} : Создатель форм GTFS начал маршрутизацию..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1222" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on the files_to_delete.json</source>
        <translation>Временные файлы будут удалены только при перезагрузке QGIS, их пути сохранены в files_to_delete.json</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1326" />
        <source>Something wrong went creating the trips, GO BACK to step 1, remove the buses concerned and try again</source>
        <translation>Что-то пошло не так при создании поездок, ВЕРНИТЕСЬ на шаг 1, удалите затронутые автобусы и попробуйте снова</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1386" />
        <source>{trip} is missing</source>
        <translation>{trip} отсутствует</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1409" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : Integrating the shapes to the GTFS file take much less time</source>
        <translation>в {datetime.datetime.now().time().replace(microsecond=0)} : Интеграция форм в файл GTFS занимает намного меньше времени</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1565" />
        <source>It's DONE! Find your file in {zip_file}, CONGRATULATION!</source>
        <translation>Это СДЕЛАНО! Найдите свой файл в {zip_file}, ПОЗДРАВЛЯЕМ!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1717" />
        <source>you have never run the plugins with the </source>
        <translation>вы никогда не запускали плагин с</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1739" />
        <source>the </source>
        <translation>на</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidgetBase</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="20" />
        <source>GTFS Shapes Creator</source>
        <translation>Создатель форм GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="42" />
        <source>Download a GTFS on opendatatransport.swiss</source>
        <translation>Загрузите GTFS на opendatatransport.swiss</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="61" />
        <source>Browse to the GTFS unzipped Folder</source>
        <translation>Перейдите в распакованную папку GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="130" />
        <source>1st step - agencies selection</source>
        <translation>1-й шаг - выбор агентств</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="148" />
        <source>Update Agencies</source>
        <translation>Обновить Агентства</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="189" />
        <source>Search the agency</source>
        <translation>Поиск агентства</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="214" />
        <source>Load the PT lines for the selected agencies</source>
        <translation>Загрузите линии PT для выбранных агентств</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="241" />
        <source>2nd step - transports selection</source>
        <translation>2-й шаг - выбор видов транспорта</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="287" />
        <source>Load the stops and create the roads/rails 
networks for the selected transports</source>
        <translation>Загрузите остановки и создайте дорожные/железнодорожные сети для выбранных видов транспорта</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="301" />
        <source>It will take lot of time, be patient...</source>
        <translation>Это займет много времени, будьте терпеливы...</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="314" />
        <source>Remove precedent loaded liens</source>
        <translation>Удалить ранее загруженные линии</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="328" />
        <source>3rd step - move the off-road stops</source>
        <translation>3-й шаг - переместить остановки вне дорог</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="365" />
        <source>Zoom on the selected Stop</source>
        <translation>Увеличить выбранную остановку</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="381" />
        <source>Create the paths for each trip</source>
        <translation>Создайте маршруты для каждой поездки</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="395" />
        <source>4th step - correct the transports paths</source>
        <translation>4-й шаг - исправить маршруты транспорта</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="407" />
        <source>Display Trips</source>
        <translation>Показать Поездки</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="440" />
        <source>Create your shapes.txt
and 
the final GTFS .zip file !</source>
        <translation>Создайте свой shapes.txt и финальный файл GTFS .zip!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="455" />
        <source>you like those trips ? .. </source>
        <translation>вам нравятся эти поездки? ..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="475" />
        <source> PUSH THE BUTTON!</source>
        <translation>НАЖМИТЕ КНОПКУ!</translation>
    </message>
</context>
</TS>