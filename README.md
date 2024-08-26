## Aither to BLU Upload Checker

This script works to check if there are movies that are available on Aither that can be uploaded to BLU. After pip installing requirements.txt, you need to replace the api keys for both Aither and BLU. 

Then, run 
```
python check_upload.py
```


Upon running the script, which is set to 30 iterations automatically, any movies that it finds on Aither and not BLU will be printed to the command line. Before uploading to BLU, be sure to check naming rules and if it is one of the banned groups.