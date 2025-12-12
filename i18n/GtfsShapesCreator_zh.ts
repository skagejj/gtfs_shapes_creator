<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1">
<context>
    <name>GtfsShapesCreator</name>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="200" />
        <source>&amp;GTFS Shapes Creator</source>
        <translation>&amp;GTFS形状生成器</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator.py" line="169" />
        <source>Create the shapes.txt for your GTFS</source>
        <translation>为您的GTFS创建shapes.txt文件</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidget</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="204" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on files_to_delete.json</source>
        <translation>临时文件仅在重启QGIS时删除,其路径保存在files_to_delete.json中</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="222" />
        <source>Starting at {datetime.datetime.now().time().replace(microsecond=0)} the real job (..be patient, please)</source>
        <translation>从{datetime.datetime.now().time().replace(microsecond=0)}开始真正的工作(..请耐心等待)</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1750" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on {files_to_delete_next_bus_loading_json}</source>
        <translation>临时文件仅在重启QGIS时删除,其路径保存在{files_to_delete_next_bus_loading_json}中</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1184" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : GTFS Shapes Creator has started routing..</source>
        <translation>在{datetime.datetime.now().time().replace(microsecond=0)}: GTFS形状生成器已开始路由..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1222" />
        <source>The temporary files will be deleted only restarting QGIS, their paths are saved on the files_to_delete.json</source>
        <translation>临时文件仅在重启QGIS时删除,其路径保存在files_to_delete.json中</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1326" />
        <source>Something wrong went creating the trips, GO BACK to step 1, remove the buses concerned and try again</source>
        <translation>创建行程时出错,请返回第1步,删除相关的公交车并重试</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1386" />
        <source>{trip} is missing</source>
        <translation>{trip}缺失</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1409" />
        <source>at {datetime.datetime.now().time().replace(microsecond=0)} : Integrating the shapes to the GTFS file take much less time</source>
        <translation>在{datetime.datetime.now().time().replace(microsecond=0)}: 将形状集成到GTFS文件花费的时间少得多</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1565" />
        <source>It's DONE! Find your file in {zip_file}, CONGRATULATION!</source>
        <translation>完成了!在{zip_file}中找到您的文件,恭喜!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1717" />
        <source>you have never run the plugins with the </source>
        <translation>您从未使用过该插件</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget.py" line="1739" />
        <source>the </source>
        <translation>该</translation>
    </message>
</context>
<context>
    <name>GtfsShapesCreatorDockWidgetBase</name>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="20" />
        <source>GTFS Shapes Creator</source>
        <translation>GTFS形状生成器</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="42" />
        <source>Download a GTFS on opendatatransport.swiss</source>
        <translation>在opendatatransport.swiss上下载GTFS</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="61" />
        <source>Browse to the GTFS unzipped Folder</source>
        <translation>浏览到GTFS解压缩的文件夹</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="130" />
        <source>1st step - agencies selection</source>
        <translation>第1步-选择机构</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="148" />
        <source>Update Agencies</source>
        <translation>更新机构</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="189" />
        <source>Search the agency</source>
        <translation>搜索机构</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="214" />
        <source>Load the PT lines for the selected agencies</source>
        <translation>为选定的机构加载PT线路</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="241" />
        <source>2nd step - transports selection</source>
        <translation>第2步-选择运输方式</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="287" />
        <source>Load the stops and create the roads/rails 
networks for the selected transports</source>
        <translation>为选定的运输方式加载站点并创建道路/铁路网络</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="301" />
        <source>It will take lot of time, be patient...</source>
        <translation>这将需要很长时间,请耐心等待...</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="314" />
        <source>Remove precedent loaded liens</source>
        <translation>删除之前加载的线路</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="328" />
        <source>3rd step - move the off-road stops</source>
        <translation>第3步-移动路外的站点</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="365" />
        <source>Zoom on the selected Stop</source>
        <translation>缩放到选定的站点</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="381" />
        <source>Create the paths for each trip</source>
        <translation>为每次行程创建路径</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="395" />
        <source>4th step - correct the transports paths</source>
        <translation>第4步-纠正运输路径</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="407" />
        <source>Display Trips</source>
        <translation>显示行程</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="440" />
        <source>Create your shapes.txt
and 
the final GTFS .zip file !</source>
        <translation>创建您的shapes.txt和最终的GTFS .zip文件!</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="455" />
        <source>you like those trips ? .. </source>
        <translation>您喜欢这些行程吗? ..</translation>
    </message>
    <message>
        <location filename="../gtfs_shapes_creator_dockwidget_base.ui" line="475" />
        <source> PUSH THE BUTTON!</source>
        <translation>按下按钮!</translation>
    </message>
</context>
</TS>