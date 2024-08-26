banned_groups = [
    "[Oj]", "3LTON", "4yEo", "ADE", "AFG", "AniHLS", "AnimeRG", "AniURL",
    "AROMA", "aXXo", "Brrip", "CHD", "CM8", "CrEwSaDe", "d3g", "DeadFish",
    "DNL", "ELiTE", "eSc", "FaNGDiNG0", "FGT", "Flights", "FRDS", "FUM",
    "HAiKU", "HD2DVD", "HDS", "HDTime", "Hi10", "ION10", "iPlanet", "JIVE",
    "KiNGDOM", "Leffe", "LEGi0N", "LOAD", "MeGusta", "mHD", "mSD", "NhaNc3",
    "nHD", "nikt0", "NOIVTC", "nSD", "OFT", "PiRaTeS", "playBD", "PlaySD",
    "playXD", "PRODJi", "RAPiDCOWS", "RARBG", "RetroPeeps", "RDN",
    "REsuRRecTioN", "RMTeam", "SANTi", "SicFoI", "SPASM", "SPDVD",
    "STUTTERSHIT", "Telly", "TM", "TRiToN", "UPiNSMOKE", "URANiME", "WAF",
    "x0r", "xRed", "XS", "YIFY", "ZKBL", "ZmN", "ZMNT"
]

def check_if_banned(str):
    for banned_group in banned_groups:
        if banned_group in str:
            return True
    return False
