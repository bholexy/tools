#!/bin/bash

# send graduation reminder
cd /tools/tool/workexp && ./wepeople.py checkstatus graduation_reminder y

# send income verification reminder
cd /tools/tool/workexp && ./wepeople.py checkstatus income_verification
