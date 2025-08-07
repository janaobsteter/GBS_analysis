tasselDir=/home/share/GBS_honeybee/tassel3-standalone/
${tasselDir}/run_pipeline.pl -fork1 -Xmx250g -Xms100g \
-BinaryToTextPlugin \
-i /home/share/GBS_honeybee/Run2/Tassel3_pipeline/ourdata/mergedTagCounts/mergedAll.cnt \
-o /home/share/GBS_honeybee/Run2/Tassel3_pipeline/ourdata/mergedTagCounts/mergedAll.txt \
-t TagCounts -endPlugin -runfork1