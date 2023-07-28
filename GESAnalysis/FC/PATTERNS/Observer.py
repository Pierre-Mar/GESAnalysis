#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
# Created By :
# Name : Marjolin Pierre
# E-Mail : pierre.marjolin@gmail.com
# Github : Pierre-Mar
#---------------------------------------------------------------------------------
class Observer:
    """ Class/Interface to update UI when there are some change
        with the data
    """
    
    def update() -> None:
        """ Method to update an observer.
            Need to overwrite it
        """
        pass
