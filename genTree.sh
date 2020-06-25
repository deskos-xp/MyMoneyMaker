echo 'mkdir -p app/Education/{forms,workers} ; touch app/Education/__init__.py ; touch app/Education/workers/__init__.py' | sed s/Education/"$1"/g
