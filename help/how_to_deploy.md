In the terminal 

cd .local/share/QGIS/QGIS3/profiles/default/python/plugins/gtfs_shapes_creator/
pyenv local 3.10.16
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pb_tool deploy
pb_tool compile
pyrcc5 -o resources.py resources.qrc 

https://plugins.qgis.org/docs/publish