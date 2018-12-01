# if TOC is not a package
# use from app import create_app is correct

# but if TOC is a package
# .app is neccessary because . means look up in the curernt package for "app"
from app import create_app

app=create_app()