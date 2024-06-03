Video presentation for the project: https://youtu.be/NN9GYnHz-g4

We opted to use the 2023 Amazon Reviews Dataset, but since it was greater than 150GB in size, we chose to merge 14 categories, whose [zipped files](https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/raw/review_categories/) were less than 1GB, or whose [total size](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/tree/bfb602ae7048495ad22a650be956e7838ceefd15/raw/review_categories) is less than 3GB. We merged samples from 14 categories, resulting in a dataset of 30,594,036 records (~15GB). The merged categories include:

- **All_Beauty**: 701,528 records
- **Appliances**: 2,128,605 records
- **Health_and_Personal_Care**: 494,121 records
- **Industrial_and_Scientific**: 5,183,005 records
- **Amazon_Fashion**: 2,500,939 records
- **Baby_Products**: 6,028,884 records
- **Subscription_Boxes**: 16,216 records
- **Handmade_Products**: 664,162 records
- **Digital_Music**: 130,434 records
- **Software**: 4,880,181 records
- **Musical_Instruments**: 3,017,439 records
- **Magazine_Subscriptions**: 71,497 records
- **Video_Games**: 4,624,615 records
- **Gift_Cards**: 152,410 records
