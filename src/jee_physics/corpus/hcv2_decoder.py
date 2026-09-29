"""
HCV Volume 2 Font-Table Decoder and Normalizer.
Forensically handles non-standard Type 3/TrueType ASCII Caesar font shifts
present in specific chapters (Chapters 23 and 30) while preserving standard text.
"""

from typing import Tuple
from jee_physics.models.evidence import ExtractionQuality


SHIFTED_WORDS = {
    "WKH", "DQG", "RI", "WR", "LQ", "LV", "WKDW", "ZLWK",
    "IURP", "DV", "E\\", "IRU", "&+$37(5", "7+(", "72", "68&+"
}

NORMAL_COMMON_WORDS = {
    "the", "and", "of", "to", "in", "is", "that", "with",
    "from", "as", "by", "for", "such", "this", "are", "have"
}


def is_hcv2_page_font_shifted(text: str) -> bool:
    """
    Deterministically determines if a page in HCV Volume 2 utilizes the
    +29 ASCII font-shift table.
    """
    if not text or not text.strip():
        return False
    words = set(text.split())
    shifted_hits = len(words.intersection(SHIFTED_WORDS))
    normal_hits = len(words.intersection(NORMAL_COMMON_WORDS))

    if "&+$37(5" in text:
        return True
    if shifted_hits >= 2 and normal_hits == 0:
        return True
    if shifted_hits > normal_hits and shifted_hits >= 3:
        return True
    return False


def decode_hcv2_text(text: str) -> str:
    """
    Decodes font-shifted ASCII characters in HCV Volume 2.
    Shifts uppercase/punctuation ASCII values by +29 (or mod 32 shift)
    into standard printable English characters, mapping '\\x03' to space.
    """
    res = []
    for c in text:
        if c in " \n\r\t":
            res.append(c)
        elif ord(c) == 3:  # \x03 is used as space delimiter in shifted font
            res.append(" ")
        else:
            val = ord(c) + 29
            if 32 <= val <= 126:
                res.append(chr(val))
            else:
                res.append(c)
    return "".join(res)


def extract_hcv2_page(raw_text: str) -> Tuple[str, bool, ExtractionQuality]:
    """
    Extracts and normalizes an HCV Volume 2 page text stream.
    Returns: (normalized_text, was_shifted, extraction_quality)
    """
    cleaned = raw_text.strip()
    if not cleaned:
        return "", False, ExtractionQuality.EMPTY

    if is_hcv2_page_font_shifted(raw_text):
        decoded = decode_hcv2_text(raw_text)
        return decoded, True, ExtractionQuality.NORMALIZED_FONT

    return raw_text, False, ExtractionQuality.EXCELLENT
