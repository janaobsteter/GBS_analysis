#bash ./01_create_dirs.sh

echo 02_FastqToTagCount
bash ./02_UFastqToTagCount.sh 2>&1 | tee 02_FastqToTagCount.log

echo 03_MergeTaxaTagCount
bash ./03_UMergeTaxaTagCount.sh 2>&1 | tee 03_MergeTaxaTagCount.log

echo 04_TagCountToTagPair
bash ./04_UTagCountToTagPair.sh 2>&1 | tee 04_TagCountToTagPair.log

echo 05_TagPairToTBT
bash ./05_UTagPairToTBT.sh 2>&1 | tee 05_TagPairToTBT.log

echo 06_TBTToMapInfo
bash ./06_UTBTToMapInfo.sh 2>&1 | tee 06_TBTToMapInfo.log

echo 07_MapInfoToHapMap
bash ./07_UMapInfoToHapMap.sh 2>&1 | tee 07_MapInfoToHapMap.log
