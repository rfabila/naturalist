#!/usr/bin/python
import os

os.chdir("/home/naturalist/naturalist")

import zoo
zoo.full_update(mail_summaries=True)
