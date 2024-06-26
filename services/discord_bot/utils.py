import discord
import gcld3
import numpy as np
from urllib3.util import parse_url


async def purge_reactions(
    message: discord.Message, member: discord.Member, current_reaction_emoji: discord.Emoji
) -> None:
    for reaction in message.reactions:
        if reaction.emoji != current_reaction_emoji.name:
            await message.remove_reaction(reaction.emoji, member)


def cosine_dist(source_embedding: np.ndarray, target_embedding: np.ndarray) -> float:
    # output similarity in range [-1, 1]
    cosine_similarity = np.dot(source_embedding, target_embedding)
    # scale to [0, 1]
    cosine_sim_scaled = (cosine_similarity + 1) / 2
    return 1 - cosine_sim_scaled


def normalize_url(url: str) -> str:
    url_parts = parse_url(url)
    if url_parts.host is None:
        raise ValueError(f"Not a properly formed url: {url}")
    clean_url = f"{url_parts.scheme if url_parts.scheme else 'http'}://"
    clean_url += url_parts.host
    clean_url = clean_url.rstrip("/")
    clean_url += f"{url_parts.path if url_parts.path else ''}"
    return clean_url


def language_detection(text: str) -> str:
    # TODO: Should this return an enum?
    detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=1000)
    result = detector.FindLanguage(text=text)
    lang_detected = result.language
    return lang_detected
