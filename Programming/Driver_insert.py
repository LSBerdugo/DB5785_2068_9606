import random

# List of Driver StaffIDs
driver_staff_ids = [
    326, 215, 149, 847, 896, 572, 217, 742, 564, 273, 31, 214, 955, 414, 365, 391, 380, 347, 454, 173,
    680, 618, 679, 232, 469, 335, 26, 406, 250, 27, 643, 935, 346, 577, 915, 314, 575, 177, 550, 376,
    422, 494, 268, 995, 983, 636, 75, 6, 746, 948, 338, 885, 952, 98, 857, 562, 988, 387, 15, 66, 254,
    543, 52, 622, 490, 305, 851, 20, 112, 210, 288, 925, 966, 982, 858, 864, 116, 559, 781, 60, 85, 78,
    728, 272, 474, 843, 478, 297, 228, 871, 764, 445, 4, 627, 295, 10, 615, 848, 197, 360, 262, 549,
    703, 936, 142, 315, 860, 629, 115, 14, 978, 602, 861, 736, 378, 449, 339, 501, 560, 286, 727, 804,
    813, 135, 820, 815, 789, 111, 740, 301, 181, 257, 502, 308, 509, 336, 154, 88, 470, 161, 141, 827,
    873, 175, 123, 483, 35, 831, 765, 747, 337, 437, 763, 892, 473, 129, 757, 921, 489, 897, 846, 557,
    348, 367, 959, 658, 814, 131, 956, 307, 826, 121, 971, 63, 356, 55, 922, 660, 561, 32, 644, 565,
    934, 828, 744, 70, 717, 89, 620, 772, 920, 110, 908, 526, 610, 732, 877, 568, 13, 792, 284, 403,
    990, 510, 539, 7, 768, 459, 614, 304, 751, 518, 917, 656, 683, 316, 968, 882, 159, 933, 193, 795,
    155, 527, 94, 227, 993, 632, 750, 923, 663, 734, 807, 646, 287, 673, 668, 946, 780, 635, 37, 443,
    93, 298, 57, 194, 991, 718, 972, 176, 260, 243, 371, 241, 576, 929, 187, 482, 282, 886, 240, 38,
    997, 869, 358, 427, 724, 987, 29, 233, 54, 900, 352, 719, 524, 531, 344, 626, 816, 942, 529, 264,
    432, 834, 355, 582, 867, 3, 71, 689, 598, 890, 498, 69, 64, 125, 492, 811, 584, 525, 280, 714, 520,
    388, 53, 354, 189, 124, 167, 800, 645, 157, 854, 677, 442, 465, 903, 313, 19, 418, 840, 472, 547,
    458, 484, 106, 145, 302, 293, 546, 249, 56, 905, 172, 143, 259, 793, 433, 685, 674, 849, 76, 538,
    405, 416, 65, 144, 822, 357, 43, 364, 994, 608, 767, 945, 156, 453, 637, 975, 477, 242, 275, 833,
    278, 889, 699, 722, 263, 5, 976, 545, 309, 516, 398, 595, 389, 246, 436, 439, 901, 165, 937, 778,
    913, 476, 980, 122, 150, 715, 184, 330, 932, 880, 803, 311, 694, 505, 438, 86, 902
]

# Open SQL file to write inserts
with open("Driver_insert.sql", "w") as file:
    file.write("INSERT INTO Driver (StaffID) VALUES\n")

    values = [f"({driver_id})" for driver_id in driver_staff_ids]

    file.write(",\n".join(values) + ";\n")

print("SQL insert statements written to Driver_insert.sql")