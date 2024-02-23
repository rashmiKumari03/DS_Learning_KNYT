# find_packages : this is responsible to finds the directories with __init__ and make it as package 
# setup : this is responsible to set up the information about the package we are creating.

# install_requires : i want all the packages we have installed in the dir will automatically fetched 
# and show in list form...for that we need to make a function get_requirements and pass 'requirements.txt' there.
# And to get everything in list form use List from typing..

# By introducing -e . in requirements.txt and install it...we can directly install setup.py too.
# Since in requirements.txt the -e . is not the package name so we need to ignore it and for that we will introduce some code here.



from setuptools import  find_packages,setup
from typing import List


HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    '''
    this fucntion will return the list of requirements
    '''

    requirements=[]
    
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()

        requirements=[req.replace('\n','') for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)



    return requirements



setup(
    name="StudentPerformance_MLP",
    version='0.0.1',
    author="Rashmi K",
    author_email='rashmik@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)



