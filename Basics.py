"""
A humble attempt at creating a Paninian vyakarana engine that acts as similar as possible to any human vaiyakarana
"""
from typing import Union
from Utilities import flatten_and_set
from Main import Padam


# global literals
l_maheshvarani = ['अइउण्', 'ऋऌक्', 'एओङ्', 'ऐऔच्', 'हयवरट्', 'लण्', 'ञमङणनम्', 'झभञ्', 'घढधष्', 'जबगडदश्', 'खफछठथचटतव्', 'कपय्', 'शषसर्', 'हल्']
d_uni_svaramap = {2366: 'आ', 2367: 'इ', 2368: 'ई', 2369: 'उ', 2370: 'ऊ', 2371: 'ऋ', 2372: 'ॠ', 2402: 'ऌ', 2375: 'ए', 2376: 'ऐ', 2379: 'ओ', 2380: 'औ'}
d_sthanamap = {'अ': 'Kantha', 'क्': 'Kantha', 'ख्': 'Kantha', 'ग्': 'Kantha', 'घ्': 'Kantha', 'ङ्': 'Kantha and Nasika', 'ह्': 'Kantha',
               'इ': 'Taalu', 'च्': 'Taalu', 'छ्': 'Taalu', 'ज्': 'Taalu', 'झ्': 'Taalu', 'ञ्': 'Taalu and Nasika', 'य्': 'Taalu', 'श्': 'Taalu',
               'ऋ': 'Moordha', 'ट्': 'Moordha', 'ठ्': 'Moordha', 'ड्': 'Moordha', 'ढ्': 'Moordha', 'ण्': 'Moordha and Nasika', 'र्': 'Moordha', 'ष्': 'Moordha',
               'ऌ': 'Danta', 'त्': 'Danta', 'थ्': 'Danta', 'द्': 'Danta', 'ध्': 'Danta', 'न्': 'Danta and Nasika', 'ल्': 'Danta', 'स्': 'Danta',
               'उ': 'Oshtham', 'प्': 'Oshtham', 'फ्': 'Oshtham', 'ब्': 'Oshtham', 'भ्': 'Oshtham', 'म्': 'Oshtham and Nasika',
               'ए': 'KanthaTaalu', 'ऐ': 'KanthaTaalu',
               'ओ': 'KanthaOshtham', 'औ': 'KanthaOshtham',
               'व्': 'DantaOshtham',
               'ं': 'Nasika', 'ः': 'Kantha'}  # The upadhmaniya, jihvamuliya are left out as they are not contextual in checking saavarnyam
d_abhyatnamap = {'क्': 'Sprshtam', 'ख्': 'Sprshtam', 'ग्': 'Sprshtam', 'घ्': 'Sprshtam', 'ङ्': 'Sprshtam', 'च्': 'Sprshtam', 'छ्': 'Sprshtam', 'ज्': 'Sprshtam', 'झ्': 'Sprshtam', 'ञ्': 'Sprshtam', 'ट्': 'Sprshtam', 'ठ्': 'Sprshtam', 'ड्': 'Sprshtam', 'ढ्': 'Sprshtam', 'ण्': 'Sprshtam', 'त्': 'Sprshtam', 'थ्': 'Sprshtam', 'द्': 'Sprshtam',
                 'ध्': 'Sprshtam', 'न्': 'Sprshtam', 'प्': 'Sprshtam', 'फ्': 'Sprshtam', 'ब्': 'Sprshtam', 'भ्': 'Sprshtam', 'म्': 'Sprshtam',
                 'य्': 'Ishad Sprshtam', 'व्': 'Ishad Sprshtam', 'र्': 'Ishad Sprshtam', 'ल्': 'Ishad Sprshtam',
                 'श्': 'Ishad Vivrutam', 'ष्': 'Ishad Vivrutam', 'स्': 'Ishad Vivrutam', 'ह्': 'Ishad Vivrutam',
                 'अ': 'Vivrutam', 'इ': 'Vivrutam', 'उ': 'Vivrutam', 'ऋ': 'Vivrutam', 'ऌ': 'Vivrutam', 'ए': 'Vivrutam', 'ओ': 'Vivrutam', 'ऐ': 'Vivrutam', 'औ': 'Vivrutam'}  # The samvrta prayatna of hrasva akara in prayoga is ignored for the same reason as above
d_bahyatnamap = {'क्': 'Vivara/Shvasa/Aghosha/Alpaprana', 'ख्': 'Vivara/Shvasa/Aghosha/Mahaprana', 'ग्': 'Samvara/Nada/Ghosha/Alpaprana', 'घ्': 'Samvara/Nada/Ghosha/Mahaprana', 'ङ्': 'Samvara/Nada/Ghosha/Alpaprana',
                 'च्': 'Vivara/Shvasa/Aghosha/Alpaprana', 'छ्': 'Vivara/Shvasa/Aghosha/Mahaprana', 'ज्': 'Samvara/Nada/Ghosha/Alpaprana', 'झ्': 'Samvara/Nada/Ghosha/Mahaprana', 'ञ्': 'Samvara/Nada/Ghosha/Alpaprana',
                 'ट्': 'Vivara/Shvasa/Aghosha/Alpaprana', 'ठ्': 'Vivara/Shvasa/Aghosha/Mahaprana', 'ड्': 'Samvara/Nada/Ghosha/Alpaprana', 'ढ्': 'Samvara/Nada/Ghosha/Mahaprana', 'ण्': 'Samvara/Nada/Ghosha/Alpaprana',
                 'त्': 'Vivara/Shvasa/Aghosha/Alpaprana', 'थ्': 'Vivara/Shvasa/Aghosha/Mahaprana', 'द्': 'Samvara/Nada/Ghosha/Alpaprana', 'ध्': 'Samvara/Nada/Ghosha/Mahaprana', 'न्': 'Samvara/Nada/Ghosha/Alpaprana',
                 'प्': 'Vivara/Shvasa/Aghosha/Alpaprana', 'फ्': 'Vivara/Shvasa/Aghosha/Mahaprana', 'ब्': 'Samvara/Nada/Ghosha/Alpaprana', 'भ्': 'Samvara/Nada/Ghosha/Mahaprana', 'म्': 'Samvara/Nada/Ghosha/Alpaprana',
                 'य्': 'Samvara/Nada/Ghosha/Alpaprana', 'व्': 'Samvara/Nada/Ghosha/Alpaprana', 'र्': 'Samvara/Nada/Ghosha/Alpaprana', 'ल्': 'Samvara/Nada/Ghosha/Alpaprana',
                 'श्': 'Vivara/Shvasa/Aghosha/Mahaprana', 'ष्': 'Vivara/Shvasa/Aghosha/Mahaprana', 'स्': 'Vivara/Shvasa/Aghosha/Mahaprana', 'ह्': 'Samvara/Nada/Ghosha/Mahaprana'}

# Ganas
Cadi = ('च', 'वा', 'ह', 'अह', 'एव', 'एवम्', 'नूनम्', 'शश्वत्', 'युगपत्', 'भूयस्', 'सूपत्', 'कूपत्', 'कुवित्', 'नेत्', 'चेत्', 'चण्', 'कच्चित्', 'यत्र', 'तत्र', 'नह', 'हन्त', 'माकिम्', 'माकीम्', 'माकिर्',
'नकिम्', 'नकीम्', 'नकिर्', 'आकीम्', 'माङ', 'नञ्', 'तावत्', 'यावत्', 'त्वा', 'त्वै', 'द्वै', 'न्वै', 'रै', 'रे', 'श्रौषट्', 'वौषट्', 'स्वाहा', 'वषट्', 'स्वधा', 'ओम्', 'तथा', 'तथाहि', 'खलु', 'किल',
'अथ', 'सुष्टु', 'स्म', 'अ', 'इ', 'उ', 'ऋ', 'ऌ', 'उ', 'ए', 'ऐ', 'ओ', 'औ', 'आदह', 'उञ्', 'उकञ्', 'वेलायाम्', 'मात्रायाम्', 'यथा', 'यत्', 'तत्', 'किम्', 'पुरा', 'वधा', 'वध्वा', 'धिक्', 'हाहा',
'हेहै', 'हहे', 'पाट्', 'प्याट्', 'आहो', 'उताहो', 'हो', 'अहो', 'नो', 'नौ', 'अथो', 'ननु', 'मन्ये', 'मिथ्या', 'असि', 'ब्रूहि', 'तु', 'नु', 'इति', 'इव', 'वत्', 'वात्', 'वन', 'बत', 'सम्', 'वशम्', 'शिकम्',
'दिकम्', 'सनुकं', 'छंवट्', 'छंबट्', 'शङ्के', 'शुकम्', 'खम्', 'सनात्', 'सनुतर्', 'नहिकम्', 'सत्यम्', 'ऋतम्', 'अद्धा', 'इद्धा', 'नोचेत्', 'नचेत्', 'नहि', 'जातु', 'कथम्', 'कुतः', 'कुत्र', 'अव', 'अनु',
'हा', 'हे', 'है', 'आहोस्वित्', 'शम्', 'कम्', 'खम्', 'दिष्ट्या', 'पशु', 'नट्', 'सह', 'आनुषट्', 'आनुषक्', 'अङ्ग', 'फट्', 'ताजक्', 'भाजक्', 'अये', 'अरे', 'वाट्', 'चाटु', 'कुम्', 'खुम्', 'घुम्', 'अम्',
'ईम्', 'सीम्', 'सिम्', 'सि', 'वै',)

Pradi = ('प्र', 'परा', 'अप', 'सम्', 'अनु', 'अव', 'निस्', 'निर्', 'दुस्', 'दुर्', 'वि', 'आङ्', 'नि', 'अधि', 'अपि', 'अति', 'सु', 'उद्', 'अभि', 'प्रति', 'परि', 'उप')
def getBaseSvara(svara: str) -> str:
    d_deerhrsv = {'आ': 'अ', 'ई': 'इ', 'ऊ': 'उ', 'ॠ': 'ऋ'}
    if svara[0] in getPratyahara('अच्', withSavarnas=False):
        return svara[0]
    elif svara[0] in d_deerhrsv.keys():
        return d_deerhrsv[svara[0]]

def getSvaraVariations(svara: str, kala: str = 'All'):
    """
    @param str svara: Any अच् can be passed
    @param str kala: Should be one of 'Hrsva', 'Deergha', 'Pluta' or 'All'
    @return tuple: Contains all variations requested, i.e. permutations of tones like udatta, etc. and anunasika or non anunasika
    """
    if svara not in ['अ', 'इ', 'उ', 'ऋ', 'ऌ', 'ए', 'ओ', 'ऐ', 'औ']:
        return ()
    if (svara == 'ऌ' and kala == 'Deergha') or (svara in ['ए', 'ओ', 'ऐ', 'औ'] and kala == 'Hrsva'):
        raise ValueError("The requested kala for the svara doesn't exist")

    end_tup, l_commons = [], ['', chr(2305), chr(2386), chr(2305) + chr(2386), chr(2385), chr(2305) + chr(2385)]
    deergha = 'आ' if svara == 'अ' else 'ई' if svara == 'इ' else 'ऊ' if svara == 'उ' else 'ॠ' if svara == 'ऋ' else ''
    for i in range(18):
        if i < 6 and (kala in ['Hrsva', 'All']) and svara not in ['ए', 'ओ', 'ऐ', 'औ']:  # hrsva
            end_tup.append(svara + l_commons[i])
        elif 6 <= i < 12 and (kala in ['Deergha', 'All']) and svara != 'ऌ':  # deergha
            if svara in ['ए', 'ओ', 'ऐ', 'औ']:  # for ए, ओ, ऐ, औ no separate roopa is there
                end_tup.append(svara + l_commons[i - 6])
            else:
                end_tup.append(deergha + l_commons[i - 6])
        elif 12 <= i < 18 and (kala in ['Pluta', 'All']):  # pluta
            end_tup.append(svara + l_commons[i - 12] + chr(2409))
    return tuple(end_tup)

def getSavarnas(letter: str):  # Based on अणुदित् सवर्णस्य चाऽप्रत्ययः (1.1.69)
    letter = getBaseSvara(letter) if getBaseSvara(letter) is not None else letter
    letter = letter[:2] if len(letter) > 1 and ord(letter[1]) == 2381 else letter

    sthana, yatna = d_sthanamap[letter], d_abhyatnamap[letter]
    l_eqsthana = [i for i in d_sthanamap if d_sthanamap[i] == sthana or (sthana in d_sthanamap[i] and 'and' in d_sthanamap[i])]
    l_eqyatna = [i for i in d_abhyatnamap if d_abhyatnamap[i] == yatna]
    tup = sorted(set(l_eqsthana).intersection(l_eqyatna))
    tup = tup[:1] if letter == 'ए' else tup[1:] if letter == 'ऐ' else tup[:1] if letter == 'ओ' else tup[1:] if letter == 'औ' else tup
    tup = ['य्', 'य्ँ'] if letter == 'य्' else ['व्', 'व्ँ'] if letter == 'व्' else ['ल्', 'ल्ँ'] if letter == 'ल्' else ['ऋ', 'ऌ'] if letter in ['ऋ', 'ऌ'] else tup
    # including all types of svaras
    if letter in ['अ', 'इ', 'उ', 'ऋ', 'ऌ', 'ए', 'ओ', 'ऐ', 'औ']:
        tup = [j for i in tup for j in getSvaraVariations(i)]  # loop on tup is for ऋ, ऌ
    return tuple(tup)

def getPratyahara(pratyahara: str, withSavarnas=True, paraNakara=False):
    if pratyahara == 'र':  # Following उपदेशेऽजनुनासिक इत् by which the अ in the middle लण् gets इत् samjna too
        return 'र्', 'ल्'
    if pratyahara == 'अण्' and paraNakara:
        return 'अ', 'इ', 'उ', 'ऋ', 'ऌ', 'ए', 'ओ', 'ऐ', 'औ', 'ह्', 'य्', 'व्', 'र्', 'ल्'
    if pratyahara in ['कु', 'चु', 'टु', 'तु', 'पु']:
        if withSavarnas:
            return getSavarnas(doPadaVigraha(pratyahara)[0])
    if pratyahara[-2:] == 'त्':
        if withSavarnas:
            if ord(pratyahara[0]) in [2309, 2311, 2313]:
                return getSvaraVariations(pratyahara[0], 'Hrsva')
            if ord(pratyahara[0]) in [2315, 2316]:
                return getSvaraVariations('ऋ', 'Hrsva') + getSvaraVariations('ऌ', 'Hrsva')
            if ord(pratyahara[0]) in [2310, 2312, 2314, 2400, 2319, 2323, 2320, 2324]:
                return getSvaraVariations(getBaseSvara(pratyahara[0]), 'Deergha')
        else:
            return pratyahara[0],

    pthara = doPadaVigraha(pratyahara)
    l_its = [i[-2:] for i in l_maheshvarani]  # list of इत् in mh sutrani. update later
    if len(pthara) > 3 or (len(pthara) == 3 and (pthara[2] not in l_its or pthara[1] != 'अ')) or (len(pthara) == 2 and (pthara[1] not in l_its)):  # restricts to only pthara of mh sutrani. update later
        raise ValueError('Please enter a valid pratyahara')
    if len(pthara) == 3:  # eliminate the अ
        pthara.pop(1)

    started, stopped, end_tup = False, False, []
    for sut in l_maheshvarani:
        s_vig = doPadaVigraha(sut)
        for i in range(len(s_vig)):
            if s_vig[i] == pthara[0] and (len(s_vig[i]) == 1 or (len(s_vig[i]) == 2 and s_vig[i] not in sut)):
                started = True
            if len(s_vig[i]) == 2 and s_vig[i] == pthara[1] and i == len(s_vig) - 1 and started:
                stopped = True

            if stopped:
                break
            if started and i != len(s_vig) - 1:
                if s_vig[i] == 'अ' and sut != 'अइउण्':
                    continue
                end_tup.append(s_vig[i])
        else:
            continue
        break
    if withSavarnas:
        new_tup = []
        for i in end_tup:
            if i in getPratyahara('अण्', paraNakara=True):
                savarnas = getSavarnas(i) if getSavarnas(i) else (i,)
                new_tup.extend(savarnas)
            else:
                new_tup.append(i)
        return flatten_and_set(tuple(new_tup))
    else:
        return flatten_and_set(tuple(end_tup))

def doPadaVigraha(expr: Union[Padam, str]) -> list:  # do for pluta and tones like udātta at a later point
    expr = expr.form if isinstance(expr, Padam) else expr
    l_vigraha = []
    for i in range(len(expr)):
        if (i + 1 == len(expr) or ord(expr[i + 1]) not in [j for j in range(2366, 2382)] + [2383, 2402]) and ord(expr[i]) in range(2325, 2362):  # if it's ending with अ
            l_vigraha.extend([expr[i] + chr(2381), chr(2309)])

        elif ord(expr[i]) in range(2325, 2362) and ord(expr[i + 1]) in [j for j in range(2366, 2381)] + [2383, 2402]:  # if it ends with अच् other than अ
            l_vigraha.extend([expr[i] + chr(2381), d_uni_svaramap[ord(expr[i + 1])]])

        elif ord(expr[i]) in range(2309, 2325) or ord(expr[i]) in [2306, 2307]:  # if it's अच् or visarga or anusvara
            l_vigraha.append(expr[i])

        elif ord(expr[i]) in range(2325, 2362) and ord(expr[i + 1]) == 2381:  # if it's हल्
            l_vigraha.append(expr[i] + chr(2381))

        elif ord(expr[i]) in [2305, 2385, 2386, 2409]:  # if it's other symbols like ३
            l_vigraha[-1] = l_vigraha[-1] + expr[i]
    return l_vigraha

def doVarnaMelana(l_varnas: list) -> str:  # do for pluta and tones like udātta at a later point
    end_str = ''
    for i in range(len(l_varnas)):
        if len(l_varnas[i]) == 3:
            if ord(l_varnas[i][2]) == 2305:
                end_str += l_varnas[i]
        elif len(l_varnas[i]) == 2:
            if (ord(l_varnas[i][0]) in range(2325, 2362) and ord(l_varnas[i][1]) == 2381) and i + 1 == len(l_varnas):
                end_str += l_varnas[i]

            # if it's like क् + अ (only अ)
            elif (ord(l_varnas[i][0]) in range(2325, 2362) and ord(l_varnas[i][1]) == 2381) and l_varnas[i + 1][0] == 'अ':  # the subscription at last condition is to avoid symbols like anusvara
                end_str += l_varnas[i][0]

            # if it's like क् + उ (not अ)
            elif (ord(l_varnas[i][0]) in range(2325, 2362) and ord(l_varnas[i][1]) == 2381) and l_varnas[i + 1][0] in d_uni_svaramap.values():
                inv_d_uni = dict(map(reversed, d_uni_svaramap.items()))
                end_str += l_varnas[i][0] + chr(inv_d_uni[l_varnas[i + 1][0]])

            # can be anunasika
            elif ord(l_varnas[i][1]) in [2305, 2385, 2386, 2409]:
                inv_d_uni = dict(map(reversed, d_uni_svaramap.items()))
                # In case a svara which has come after a svara over a halanta. Like हुआ
                if end_str and ((l_varnas[i][0] == 'अ' and ord(end_str[-1]) in range(2325, 2362)) or (l_varnas[i][0] in d_uni_svaramap.values() and ord(end_str[-1]) == inv_d_uni[l_varnas[i][0]])):
                    end_str += l_varnas[i][1]
                else:
                    end_str += l_varnas[i]

            # must be a halanta
            else:
                end_str += l_varnas[i]

        elif len(l_varnas[i]) == 1:
            if ord(l_varnas[i]) in range(2309, 2325):
                inv_d_uni = dict(map(reversed, d_uni_svaramap.items()))
                if not end_str or ((l_varnas[i] == 'अ' and ord(end_str[-1]) not in range(2325, 2362)) or (l_varnas[i] in d_uni_svaramap.values() and ord(end_str[-1]) != inv_d_uni[l_varnas[i]])) or (l_varnas[i - 1] == l_varnas[i]):  # if it's the beginning or there was another different svara before
                    end_str += l_varnas[i]

            elif ord(l_varnas[i]) in [32, 2307, 2306]:
                end_str += l_varnas[i]

    return end_str

if __name__ == '__main__':
    print(getSvaraVariations('अ', 'Pluta'))