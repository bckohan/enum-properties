"""The standard enum type for ISO 3166-1 common countrys"""

from typing_extensions import Annotated
from enum_properties import EnumProperties, Symmetric


class ISOCountry(EnumProperties):
    """
    An enumeration for ISO 3166-1 Country codes.
    """

    alpha2: Annotated[str, Symmetric(case_fold=True)]
    alpha3: Annotated[str, Symmetric(case_fold=True)]
    independent: bool
    short_name: Annotated[str, Symmetric(case_fold=True)]
    full_name: Annotated[str, Symmetric(case_fold=True)]

    # pylint: disable=C0303
    AD = 20, "AD", "AND", True, "Andorra", "the Principality of Andorra"
    AE = (
        784,
        "AE",
        "ARE",
        True,
        "United Arab Emirates (the)",
        "the United Arab Emirates",
    )
    AF = 4, "AF", "AFG", True, "Afghanistan", "the Islamic Republic of Afghanistan"
    AG = 28, "AG", "ATG", True, "Antigua and Barbuda", "Antigua and Barbuda"
    AI = 660, "AI", "AIA", False, "Anguilla", "Anguilla"
    AL = 8, "AL", "ALB", True, "Albania", "the Republic of Albania"
    AM = 51, "AM", "ARM", True, "Armenia", "the Republic of Armenia"
    AO = 24, "AO", "AGO", True, "Angola", "the Republic of Angola"
    AQ = 10, "AQ", "ATA", False, "Antarctica", "Antarctica"
    AR = 32, "AR", "ARG", True, "Argentina", "the Argentine Republic"
    AS = 16, "AS", "ASM", False, "American Samoa", "American Samoa"
    AT = 40, "AT", "AUT", True, "Austria", "the Republic of Austria"
    AU = 36, "AU", "AUS", True, "Australia", "Australia"
    AW = 533, "AW", "ABW", False, "Aruba", "Aruba"
    AX = 248, "AX", "ALA", False, "Åland Islands", "Åland Islands"
    AZ = 31, "AZ", "AZE", True, "Azerbaijan", "the Republic of Azerbaijan"
    BA = 70, "BA", "BIH", True, "Bosnia and Herzegovina", "Bosnia and Herzegovina"
    BB = 52, "BB", "BRB", True, "Barbados", "Barbados"
    BD = 50, "BD", "BGD", True, "Bangladesh", "the People's Republic of Bangladesh"
    BE = 56, "BE", "BEL", True, "Belgium", "the Kingdom of Belgium"
    BF = 854, "BF", "BFA", True, "Burkina Faso", "Burkina Faso"
    BG = 100, "BG", "BGR", True, "Bulgaria", "the Republic of Bulgaria"
    BH = 48, "BH", "BHR", True, "Bahrain", "the Kingdom of Bahrain"
    BI = 108, "BI", "BDI", True, "Burundi", "the Republic of Burundi"
    BJ = 204, "BJ", "BEN", True, "Benin", "the Republic of Benin"
    BL = 652, "BL", "BLM", False, "Saint Barthélemy", "Saint Barthélemy"
    BM = 60, "BM", "BMU", False, "Bermuda", "Bermuda"
    BN = 96, "BN", "BRN", True, "Brunei Darussalam", "Brunei Darussalam"
    BO = (
        68,
        "BO",
        "BOL",
        True,
        "Bolivia (Plurinational State of)",
        "the Plurinational State of Bolivia",
    )
    BQ = (
        535,
        "BQ",
        "BES",
        False,
        "Bonaire, Sint Eustatius and Saba",
        "Bonaire, Sint Eustatius and Saba",
    )
    BR = 76, "BR", "BRA", True, "Brazil", "the Federative Republic of Brazil"
    BS = 44, "BS", "BHS", True, "Bahamas (the)", "the Commonwealth of the Bahamas"
    BT = 64, "BT", "BTN", True, "Bhutan", "the Kingdom of Bhutan"
    BV = 74, "BV", "BVT", False, "Bouvet Island", "Bouvet Island"
    BW = 72, "BW", "BWA", True, "Botswana", "the Republic of Botswana"
    BY = 112, "BY", "BLR", True, "Belarus", "the Republic of Belarus"
    BZ = 84, "BZ", "BLZ", True, "Belize", "Belize"
    CA = 124, "CA", "CAN", True, "Canada", "Canada"
    CC = (
        166,
        "CC",
        "CCK",
        False,
        "Cocos (Keeling) Islands (the)",
        "Cocos (Keeling) Islands (the)",
    )
    CD = (
        180,
        "CD",
        "COD",
        True,
        "Congo (the Democratic Republic of the)",
        "the Democratic Republic of the Congo",
    )
    CF = (
        140,
        "CF",
        "CAF",
        True,
        "Central African Republic (the)",
        "the Central African Republic",
    )
    CG = 178, "CG", "COG", True, "Congo (the)", "the Republic of the Congo"
    CH = 756, "CH", "CHE", True, "Switzerland", "the Swiss Confederation"
    CI = 384, "CI", "CIV", True, "Côte d'Ivoire", "the Republic of Côte d'Ivoire"
    CK = 184, "CK", "COK", False, "Cook Islands (the)", "Cook Islands (the)"
    CL = 152, "CL", "CHL", True, "Chile", "the Republic of Chile"
    CM = 120, "CM", "CMR", True, "Cameroon", "the Republic of Cameroon"
    CN = 156, "CN", "CHN", True, "China", "the People's Republic of China"
    CO = 170, "CO", "COL", True, "Colombia", "the Republic of Colombia"
    CR = 188, "CR", "CRI", True, "Costa Rica", "the Republic of Costa Rica"
    CU = 192, "CU", "CUB", True, "Cuba", "the Republic of Cuba"
    CV = 132, "CV", "CPV", True, "Cabo Verde", "the Republic of Cabo Verde"
    CW = 531, "CW", "CUW", False, "Curaçao", "Curaçao"
    CX = 162, "CX", "CXR", False, "Christmas Island", "Christmas Island"
    CY = 196, "CY", "CYP", True, "Cyprus", "the Republic of Cyprus"
    CZ = 203, "CZ", "CZE", True, "Czechia", "the Czech Republic"
    DE = 276, "DE", "DEU", True, "Germany", "the Federal Republic of Germany"
    DJ = 262, "DJ", "DJI", True, "Djibouti", "the Republic of Djibouti"
    DK = 208, "DK", "DNK", True, "Denmark", "the Kingdom of Denmark"
    DM = 212, "DM", "DMA", True, "Dominica", "the Commonwealth of Dominica"
    DO = 214, "DO", "DOM", True, "Dominican Republic (the)", "the Dominican Republic"
    DZ = 12, "DZ", "DZA", True, "Algeria", "the People's Democratic Republic of Algeria"
    EC = 218, "EC", "ECU", True, "Ecuador", "the Republic of Ecuador"
    EE = 233, "EE", "EST", True, "Estonia", "the Republic of Estonia"
    EG = 818, "EG", "EGY", True, "Egypt", "the Arab Republic of Egypt"
    EH = 732, "EH", "ESH", False, "Western Sahara*", "Western Sahara*"
    ER = 232, "ER", "ERI", True, "Eritrea", "the State of Eritrea"
    ES = 724, "ES", "ESP", True, "Spain", "the Kingdom of Spain"
    ET = (
        231,
        "ET",
        "ETH",
        True,
        "Ethiopia",
        "the Federal Democratic Republic of Ethiopia",
    )
    FI = 246, "FI", "FIN", True, "Finland", "the Republic of Finland"
    FJ = 242, "FJ", "FJI", True, "Fiji", "the Republic of Fiji"
    FK = (
        238,
        "FK",
        "FLK",
        False,
        "Falkland Islands (the) [Malvinas]",
        "Falkland Islands (the) [Malvinas]",
    )
    FM = (
        583,
        "FM",
        "FSM",
        True,
        "Micronesia (Federated States of)",
        "the Federated States of Micronesia",
    )
    FO = 234, "FO", "FRO", False, "Faroe Islands (the)", "Faroe Islands (the)"
    FR = 250, "FR", "FRA", True, "France", "the French Republic"
    GA = 266, "GA", "GAB", True, "Gabon", "the Gabonese Republic"
    GB = (
        826,
        "GB",
        "GBR",
        True,
        "United Kingdom of Great Britain and Northern Ireland (the)",
        "the United Kingdom of Great Britain and Northern Ireland",
    )
    GD = 308, "GD", "GRD", True, "Grenada", "Grenada"
    GE = 268, "GE", "GEO", True, "Georgia", "Georgia"
    GF = 254, "GF", "GUF", False, "French Guiana", "French Guiana"
    GG = 831, "GG", "GGY", False, "Guernsey", "Guernsey"
    GH = 288, "GH", "GHA", True, "Ghana", "the Republic of Ghana"
    GI = 292, "GI", "GIB", False, "Gibraltar", "Gibraltar"
    GL = 304, "GL", "GRL", False, "Greenland", "Greenland"
    GM = 270, "GM", "GMB", True, "Gambia (the)", "the Republic of the Gambia"
    GN = 324, "GN", "GIN", True, "Guinea", "the Republic of Guinea"
    GP = 312, "GP", "GLP", False, "Guadeloupe", "Guadeloupe"
    GQ = (
        226,
        "GQ",
        "GNQ",
        True,
        "Equatorial Guinea",
        "the Republic of Equatorial Guinea",
    )
    GR = 300, "GR", "GRC", True, "Greece", "the Hellenic Republic"
    GS = (
        239,
        "GS",
        "SGS",
        False,
        "South Georgia and the South Sandwich Islands",
        "South Georgia and the South Sandwich Islands",
    )
    GT = 320, "GT", "GTM", True, "Guatemala", "the Republic of Guatemala"
    GU = 316, "GU", "GUM", False, "Guam", "Guam"
    GW = 624, "GW", "GNB", True, "Guinea-Bissau", "the Republic of Guinea-Bissau"
    GY = 328, "GY", "GUY", True, "Guyana", "the Co-operative Republic of Guyana"
    HK = (
        344,
        "HK",
        "HKG",
        False,
        "Hong Kong",
        "the Hong Kong Special Administrative Region of China",
    )
    HM = (
        334,
        "HM",
        "HMD",
        False,
        "Heard Island and McDonald Islands",
        "Heard Island and McDonald Islands",
    )
    HN = 340, "HN", "HND", True, "Honduras", "the Republic of Honduras"
    HR = 191, "HR", "HRV", True, "Croatia", "the Republic of Croatia"
    HT = 332, "HT", "HTI", True, "Haiti", "the Republic of Haiti"
    HU = 348, "HU", "HUN", True, "Hungary", "Hungary"
    ID = 360, "ID", "IDN", True, "Indonesia", "the Republic of Indonesia"
    IE = 372, "IE", "IRL", True, "Ireland", "Ireland"
    IL = 376, "IL", "ISR", True, "Israel", "the State of Israel"
    IM = 833, "IM", "IMN", False, "Isle of Man", "Isle of Man"
    IN = 356, "IN", "IND", True, "India", "the Republic of India"
    IO = (
        86,
        "IO",
        "IOT",
        False,
        "British Indian Ocean Territory (the)",
        "British Indian Ocean Territory (the)",
    )
    IQ = 368, "IQ", "IRQ", True, "Iraq", "the Republic of Iraq"
    IR = (
        364,
        "IR",
        "IRN",
        True,
        "Iran (Islamic Republic of)",
        "the Islamic Republic of Iran",
    )
    IS = 352, "IS", "ISL", True, "Iceland", "the Republic of Iceland"
    IT = 380, "IT", "ITA", True, "Italy", "the Republic of Italy"
    JE = 832, "JE", "JEY", False, "Jersey", "Jersey"
    JM = 388, "JM", "JAM", True, "Jamaica", "Jamaica"
    JO = 400, "JO", "JOR", True, "Jordan", "the Hashemite Kingdom of Jordan"
    JP = 392, "JP", "JPN", True, "Japan", "Japan"
    KE = 404, "KE", "KEN", True, "Kenya", "the Republic of Kenya"
    KG = 417, "KG", "KGZ", True, "Kyrgyzstan", "the Kyrgyz Republic"
    KH = 116, "KH", "KHM", True, "Cambodia", "the Kingdom of Cambodia"
    KI = 296, "KI", "KIR", True, "Kiribati", "the Republic of Kiribati"
    KM = 174, "KM", "COM", True, "Comoros (the)", "the Union of the Comoros"
    KN = 659, "KN", "KNA", True, "Saint Kitts and Nevis", "Saint Kitts and Nevis"
    KP = (
        408,
        "KP",
        "PRK",
        True,
        "Korea (the Democratic People's Republic of)",
        "the Democratic People's Republic of Korea",
    )
    KR = 410, "KR", "KOR", True, "Korea (the Republic of)", "the Republic of Korea"
    KW = 414, "KW", "KWT", True, "Kuwait", "the State of Kuwait"
    KY = 136, "KY", "CYM", False, "Cayman Islands (the)", "Cayman Islands (the)"
    KZ = 398, "KZ", "KAZ", True, "Kazakhstan", "the Republic of Kazakhstan"
    LA = (
        418,
        "LA",
        "LAO",
        True,
        "Lao People's Democratic Republic (the)",
        "the Lao People's Democratic Republic",
    )
    LB = 422, "LB", "LBN", True, "Lebanon", "the Lebanese Republic"
    LC = 662, "LC", "LCA", True, "Saint Lucia", "Saint Lucia"
    LI = 438, "LI", "LIE", True, "Liechtenstein", "the Principality of Liechtenstein"
    LK = (
        144,
        "LK",
        "LKA",
        True,
        "Sri Lanka",
        "the Democratic Socialist Republic of Sri Lanka",
    )
    LR = 430, "LR", "LBR", True, "Liberia", "the Republic of Liberia"
    LS = 426, "LS", "LSO", True, "Lesotho", "the Kingdom of Lesotho"
    LT = 440, "LT", "LTU", True, "Lithuania", "the Republic of Lithuania"
    LU = 442, "LU", "LUX", True, "Luxembourg", "the Grand Duchy of Luxembourg"
    LV = 428, "LV", "LVA", True, "Latvia", "the Republic of Latvia"
    LY = 434, "LY", "LBY", True, "Libya", "the State of Libya"
    MA = 504, "MA", "MAR", True, "Morocco", "the Kingdom of Morocco"
    MC = 492, "MC", "MCO", True, "Monaco", "the Principality of Monaco"
    MD = 498, "MD", "MDA", True, "Moldova (the Republic of)", "the Republic of Moldova"
    ME = 499, "ME", "MNE", True, "Montenegro", "Montenegro"
    MF = (
        663,
        "MF",
        "MAF",
        False,
        "Saint Martin (French part)",
        "Saint Martin (French part)",
    )
    MG = 450, "MG", "MDG", True, "Madagascar", "the Republic of Madagascar"
    MH = (
        584,
        "MH",
        "MHL",
        True,
        "Marshall Islands (the)",
        "the Republic of the Marshall Islands",
    )
    MK = 807, "MK", "MKD", True, "North Macedonia", "the Republic of North Macedonia"
    ML = 466, "ML", "MLI", True, "Mali", "the Republic of Mali"
    MM = 104, "MM", "MMR", True, "Myanmar", "the Republic of the Union of Myanmar"
    MN = 496, "MN", "MNG", True, "Mongolia", "Mongolia"
    MO = (
        446,
        "MO",
        "MAC",
        False,
        "Macao",
        "Macao Special Administrative Region of China",
    )
    MP = (
        580,
        "MP",
        "MNP",
        False,
        "Northern Mariana Islands (the)",
        "the Commonwealth of the Northern Mariana Islands",
    )
    MQ = 474, "MQ", "MTQ", False, "Martinique", "Martinique"
    MR = 478, "MR", "MRT", True, "Mauritania", "the Islamic Republic of Mauritania"
    MS = 500, "MS", "MSR", False, "Montserrat", "Montserrat"
    MT = 470, "MT", "MLT", True, "Malta", "the Republic of Malta"
    MU = 480, "MU", "MUS", True, "Mauritius", "the Republic of Mauritius"
    MV = 462, "MV", "MDV", True, "Maldives", "the Republic of Maldives"
    MW = 454, "MW", "MWI", True, "Malawi", "the Republic of Malawi"
    MX = 484, "MX", "MEX", True, "Mexico", "the United Mexican States"
    MY = 458, "MY", "MYS", True, "Malaysia", "Malaysia"
    MZ = 508, "MZ", "MOZ", True, "Mozambique", "the Republic of Mozambique"
    NA = 516, "NA", "NAM", True, "Namibia", "the Republic of Namibia"
    NC = 540, "NC", "NCL", False, "New Caledonia", "New Caledonia"
    NE = 562, "NE", "NER", True, "Niger (the)", "the Republic of the Niger"
    NF = 574, "NF", "NFK", False, "Norfolk Island", "Norfolk Island"
    NG = 566, "NG", "NGA", True, "Nigeria", "the Federal Republic of Nigeria"
    NI = 558, "NI", "NIC", True, "Nicaragua", "the Republic of Nicaragua"
    NL = 528, "NL", "NLD", True, "Netherlands (the)", "the Kingdom of the Netherlands"
    NO = 578, "NO", "NOR", True, "Norway", "the Kingdom of Norway"
    NP = 524, "NP", "NPL", True, "Nepal", "Nepal"
    NR = 520, "NR", "NRU", True, "Nauru", "the Republic of Nauru"
    NU = 570, "NU", "NIU", False, "Niue", "Niue"
    NZ = 554, "NZ", "NZL", True, "New Zealand", "New Zealand"
    OM = 512, "OM", "OMN", True, "Oman", "the Sultanate of Oman"
    PA = 591, "PA", "PAN", True, "Panama", "the Republic of Panama"
    PE = 604, "PE", "PER", True, "Peru", "the Republic of Peru"
    PF = 258, "PF", "PYF", False, "French Polynesia", "French Polynesia"
    PG = (
        598,
        "PG",
        "PNG",
        True,
        "Papua New Guinea",
        "the Independent State of Papua New Guinea",
    )
    PH = 608, "PH", "PHL", True, "Philippines (the)", "the Republic of the Philippines"
    PK = 586, "PK", "PAK", True, "Pakistan", "the Islamic Republic of Pakistan"
    PL = 616, "PL", "POL", True, "Poland", "the Republic of Poland"
    PM = (
        666,
        "PM",
        "SPM",
        False,
        "Saint Pierre and Miquelon",
        "Saint Pierre and Miquelon",
    )
    PN = 612, "PN", "PCN", False, "Pitcairn", "Pitcairn"
    PR = 630, "PR", "PRI", False, "Puerto Rico", "Puerto Rico"
    PS = 275, "PS", "PSE", False, "Palestine, State of", "the State of Palestine"
    PT = 620, "PT", "PRT", True, "Portugal", "the Portuguese Republic"
    PW = 585, "PW", "PLW", True, "Palau", "the Republic of Palau"
    PY = 600, "PY", "PRY", True, "Paraguay", "the Republic of Paraguay"
    QA = 634, "QA", "QAT", True, "Qatar", "the State of Qatar"
    RE = 638, "RE", "REU", False, "Réunion", "Réunion"
    RO = 642, "RO", "ROU", True, "Romania", "Romania"
    RS = 688, "RS", "SRB", True, "Serbia", "the Republic of Serbia"
    RU = 643, "RU", "RUS", True, "Russian Federation (the)", "the Russian Federation"
    RW = 646, "RW", "RWA", True, "Rwanda", "the Republic of Rwanda"
    SA = 682, "SA", "SAU", True, "Saudi Arabia", "the Kingdom of Saudi Arabia"
    SB = 90, "SB", "SLB", True, "Solomon Islands", "Solomon Islands"
    SC = 690, "SC", "SYC", True, "Seychelles", "the Republic of Seychelles"
    SD = 729, "SD", "SDN", True, "Sudan (the)", "the Republic of the Sudan"
    SE = 752, "SE", "SWE", True, "Sweden", "the Kingdom of Sweden"
    SG = 702, "SG", "SGP", True, "Singapore", "the Republic of Singapore"
    SH = (
        654,
        "SH",
        "SHN",
        False,
        "Saint Helena, Ascension and Tristan da Cunha",
        "Saint Helena, Ascension and Tristan da Cunha",
    )
    SI = 705, "SI", "SVN", True, "Slovenia", "the Republic of Slovenia"
    SJ = 744, "SJ", "SJM", False, "Svalbard and Jan Mayen", "Svalbard and Jan Mayen"
    SK = 703, "SK", "SVK", True, "Slovakia", "the Slovak Republic"
    SL = 694, "SL", "SLE", True, "Sierra Leone", "the Republic of Sierra Leone"
    SM = 674, "SM", "SMR", True, "San Marino", "the Republic of San Marino"
    SN = 686, "SN", "SEN", True, "Senegal", "the Republic of Senegal"
    SO = 706, "SO", "SOM", True, "Somalia", "the Federal Republic of Somalia"
    SR = 740, "SR", "SUR", True, "Suriname", "the Republic of Suriname"
    SS = 728, "SS", "SSD", True, "South Sudan", "the Republic of South Sudan"
    ST = (
        678,
        "ST",
        "STP",
        True,
        "Sao Tome and Principe",
        "the Democratic Republic of Sao Tome and Principe",
    )
    SV = 222, "SV", "SLV", True, "El Salvador", "the Republic of El Salvador"
    SX = (
        534,
        "SX",
        "SXM",
        False,
        "Sint Maarten (Dutch part)",
        "Sint Maarten (Dutch part)",
    )
    SY = (
        760,
        "SY",
        "SYR",
        True,
        "Syrian Arab Republic (the)",
        "the Syrian Arab Republic",
    )
    SZ = 748, "SZ", "SWZ", True, "Eswatini", "the Kingdom of Eswatini"
    TC = (
        796,
        "TC",
        "TCA",
        False,
        "Turks and Caicos Islands (the)",
        "Turks and Caicos Islands (the)",
    )
    TD = 148, "TD", "TCD", True, "Chad", "the Republic of Chad"
    TF = (
        260,
        "TF",
        "ATF",
        False,
        "French Southern Territories (the)",
        "French Southern Territories (the)",
    )
    TG = 768, "TG", "TGO", True, "Togo", "the Togolese Republic"
    TH = 764, "TH", "THA", True, "Thailand", "the Kingdom of Thailand"
    TJ = 762, "TJ", "TJK", True, "Tajikistan", "the Republic of Tajikistan"
    TK = 772, "TK", "TKL", False, "Tokelau", "Tokelau"
    TL = 626, "TL", "TLS", True, "Timor-Leste", "the Democratic Republic of Timor-Leste"
    TM = 795, "TM", "TKM", True, "Turkmenistan", "Turkmenistan"
    TN = 788, "TN", "TUN", True, "Tunisia", "the Republic of Tunisia"
    TO = 776, "TO", "TON", True, "Tonga", "the Kingdom of Tonga"
    TR = 792, "TR", "TUR", True, "Türkiye", "the Republic of Türkiye"
    TT = (
        780,
        "TT",
        "TTO",
        True,
        "Trinidad and Tobago",
        "the Republic of Trinidad and Tobago",
    )
    TV = 798, "TV", "TUV", True, "Tuvalu", "Tuvalu"
    TW = (
        158,
        "TW",
        "TWN",
        False,
        "Taiwan (Province of China)",
        "Taiwan (Province of China)",
    )
    TZ = (
        834,
        "TZ",
        "TZA",
        True,
        "Tanzania, the United Republic of",
        "the United Republic of Tanzania",
    )
    UA = 804, "UA", "UKR", True, "Ukraine", "Ukraine"
    UG = 800, "UG", "UGA", True, "Uganda", "the Republic of Uganda"
    UM = (
        581,
        "UM",
        "UMI",
        False,
        "United States Minor Outlying Islands (the)",
        "United States Minor Outlying Islands (the)",
    )
    US = (
        840,
        "US",
        "USA",
        True,
        "United States of America (the)",
        "the United States of America",
    )
    UY = 858, "UY", "URY", True, "Uruguay", "the Eastern Republic of Uruguay"
    UZ = 860, "UZ", "UZB", True, "Uzbekistan", "the Republic of Uzbekistan"
    VA = 336, "VA", "VAT", True, "Holy See (the)", "Holy See (the)"
    VC = (
        670,
        "VC",
        "VCT",
        True,
        "Saint Vincent and the Grenadines",
        "Saint Vincent and the Grenadines",
    )
    VE = (
        862,
        "VE",
        "VEN",
        True,
        "Venezuela (Bolivarian Republic of)",
        "the Bolivarian Republic of Venezuela",
    )
    VG = (
        92,
        "VG",
        "VGB",
        False,
        "Virgin Islands (British)",
        "British Virgin Islands (the)",
    )
    VI = (
        850,
        "VI",
        "VIR",
        False,
        "Virgin Islands (U.S.)",
        "the Virgin Islands of the United States",
    )
    VN = 704, "VN", "VNM", True, "Viet Nam", "the Socialist Republic of Viet Nam"
    VU = 548, "VU", "VUT", True, "Vanuatu", "the Republic of Vanuatu"
    WF = 876, "WF", "WLF", False, "Wallis and Futuna", "Wallis and Futuna Islands"
    WS = 882, "WS", "WSM", True, "Samoa", "the Independent State of Samoa"
    YE = 887, "YE", "YEM", True, "Yemen", "the Republic of Yemen"
    YT = 175, "YT", "MYT", False, "Mayotte", "Mayotte"
    ZA = 710, "ZA", "ZAF", True, "South Africa", "the Republic of South Africa"
    ZM = 894, "ZM", "ZMB", True, "Zambia", "the Republic of Zambia"
    ZW = 716, "ZW", "ZWE", True, "Zimbabwe", "the Republic of Zimbabwe"
