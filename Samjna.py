from Basics import getBaseSvara, getPratyahara, doPadaVigraha, d_sthanamap, d_abhyatnamap, Cadi, Pradi, getSvaraVariations


# Samjna checks
def isHrsva(letter1: str) -> bool:
    if letter1 in [j for i in ['अ', 'इ', 'उ', 'ऋ'] for j in getPratyahara(i + 'त्')]:
        return True
    return False

def isDeergha(letter1: str) -> bool:
    if letter1 in [j for i in ['आ', 'ई', 'ऊ', 'ॠ', 'ए', 'ओ', 'ऐ', 'औ'] for j in getPratyahara(i + 'त्')]:
        return True
    return False

def isPluta(letter1: str) -> bool:
    if letter1 in [j for i in ['अ', 'इ', 'उ', 'ऋ', 'आ', 'ई', 'ऊ', 'ॠ', 'ए', 'ओ', 'ऐ', 'औ'] for j in getSvaraVariations(i, 'Pluta')]:
        return True
    return False

def isSavarna(letter1: str, letter2: str) -> bool:
    # if padavigraha has check for udātta, etc. and anunasika symbols, it can be used for validating args here
    if letter1 == letter2:
        raise ValueError("There is no savarna check for one letter")

    letter1 = getBaseSvara(letter1) if letter1 in getPratyahara('अच्') else letter1[:2]
    letter2 = getBaseSvara(letter2) if letter2 in getPratyahara('अच्') else letter2[:2]
    if letter1 == 'ऋ' and letter2 == 'ऌ':
        return True
    if (letter1 in ['ए', 'ऐ'] and letter2 in ['ए', 'ऐ']) or (letter1 in ['ओ', 'औ'] and letter2 in ['ओ', 'औ']):
        return False
    try:
        if d_sthanamap[letter1] == d_sthanamap[letter2] and d_abhyatnamap[letter1] == d_abhyatnamap[letter2]:
            return True
    except KeyError:
        raise ValueError('Pass letters with only a single character')
    return False

def isGuna(letter1: str) -> bool:
    if letter1 in getGunas():
        return True
    return False

def isVriddhi(letter1: str) -> bool:
    if letter1 in getVriddhis():
        return True
    return False

def isAnunasika(letter: str) -> bool:
    if chr(2305) in letter or letter[0] in ['ङ', 'ञ', 'ण', 'न', 'म']:
        return True

def isNipata(word: str) -> bool:
    if word in Cadi + Pradi:
        return True

def isPragruhya(word: str) -> bool:
    l_word = doPadaVigraha(word)
    if isNipata(word) and (len([i for i in l_word if i in getPratyahara('अच्')]) == 1 or l_word[-1] == 'ओ'):
        return True

def isPadam(expr: str) -> bool:
    pass


def getGunas(withsavarnas=True):
    return getPratyahara('अत्', withSavarnas=withsavarnas) + getPratyahara('एङ्', withSavarnas=withsavarnas)

def getVriddhis(withsavarnas=True):
    return getPratyahara('आत्', withSavarnas=withsavarnas) + getPratyahara('ऐच्', withSavarnas=withsavarnas)