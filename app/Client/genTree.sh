echo 'mkdir -p Education/{forms,workers} ; touch Education/__init__.py ; touch Education/workers/__init__.py' | sed s/Education/"$1"/g
