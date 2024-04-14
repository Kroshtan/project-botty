import numpy as np


async def purge_reactions(message, member, current_reaction_emoji):
    for reaction in message.reactions:
        if reaction.emoji != current_reaction_emoji.name:
            await message.remove_reaction(reaction.emoji, member)


def cosine_dist(source_embedding, target_embedding):
    # output similarity in range [-1, 1]
    cosine_similarity = np.dot(source_embedding, target_embedding)
    # scale to [0, 1]
    cosine_sim_scaled = (cosine_similarity + 1) / 2
    return 1 - cosine_sim_scaled
