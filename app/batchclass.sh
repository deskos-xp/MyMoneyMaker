for i in ${f[@]} ; do
{ cat << EOF
class $i:
 def __init__(self,auth,parent):
  self.auth=auth
  self.parent=parent
EOF
} | sed 's/Client\///g' > $i/$(echo $i | sed s/'Client\///g').py
done

