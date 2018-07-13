## Go Builder ##
This is a small builder tool For GOLANG to build executables for multiple operating systems

![picture alt](https://usm.maine.edu/sites/default/files/styles/dept_info_block/public/facilities/Facilities_InfoBlock_Tools.jpg "Go Builder")


## Compatibility ##
* Python 2.7
* Python 3

## Requirements ##
* GOLANG Setup
* Python 2.7 OR 3

## Usage ##
Simply execute script go-builder.py with python 2.7 or python 3. Following are the arguments list:

    * -d, --dest      =>  Valid root path of GO package or program you want to build
    
    * -b, --builds    =>  Colon-(:) seperated OS and Architecture list 
                          OS and Architecture in the list will be seperated by forward-slash (/)
                          _Example_: windows/386:linux/amd64 -- Here list is seprated by Colon (:)
                          means 2 elemets in list and elements have operating system and architecture
                          seprated by forward slash (/)
    
    * -o, -output     =>  Path where you need output builds (`sudo` rights needed to create directory 
                                                            and build file in restricted folders)
    
    * -p, --gopath    =>  Valid `GOPATH` path if you don't have it configured on OS level and 
                          want to set it in script explicitly
    
    * -r, --goroot    =>  Valid `GOROOT` path if you don't have it configured on OS level and 
                          want to set it in script explicitly
                          
    * -x, --exec      =>  Valid `GO` executable path if you don't have it configured on OS level 
                          and want to set it in script explicitly Default executable is `go` 
                          and will be used like this is build command: `go build xxx`
                          
 ## Contribution ##
 You can add any exciting feature you like and contribute in this small tool. if you found any bug, you can open issue or give pull request *(with fix obviously)* 
 
