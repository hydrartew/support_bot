import aiogram

from loader import dp


# удалить предыдущую инлайн клавиатуру(-ы)
async def delete_ikb(user_id, message_id):
    try:
        await dp.bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=message_id-1,
            reply_markup=None
        )
    except aiogram.utils.exceptions.MessageCantBeEdited:
        pass
    except aiogram.utils.exceptions.MessageToEditNotFound:
        pass
    except aiogram.utils.exceptions.MessageNotModified:
        pass
