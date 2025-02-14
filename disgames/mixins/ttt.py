import discord
from discord.ext import commands
import random
from ..utils import Board
from ..utils import edit_board, format_board

class TicTacToe(commands.Cog):
    """
    Tic Tac Toe command
    """

    def __init__(self, bot):
        self.bot = bot

    def get_empty(self, board):
        bord = eval(str(board))
        lst = []
        for i in range(len(bord)):
            for h in range(len(bord[i])):
                try:
                    if bord[i+1][h+1] == board.seperator:
                        lst.append(str(i+1)+str(h+1))
                except IndexError:
                    pass
        return lst or 0

    def make_random_move(self, board):
        h = self.get_empty(board)
        h = random.choice(h)
        return edit_board(board, [h], 'o')

    def make_move(self, answer, board, turn):
        bord = eval(str(board))
        if answer not in [
            "11",
            "12",
            "13",
            "21",
            "22",
            "23",
            "31",
            "32",
            "33",
        ]:
            return (
                False,
                f"Invalid Syntax: {answer} isn't a valid place on the board, Please try again",
            )
        else:
            if bord[int(answer[0])][int(answer[1])] != board.seperator:
                return (
                    False,
                    f"Invalid Syntax: {answer} has already been chosen, Please try again",
                )
            else:
                return (True, edit_board(board, [answer], turn))

    def has_won(self, board, turn):
        BLANK = board.seperator
        bord = eval(str(board))
        h = 0
        for i in bord:
            for thing in i:
                if thing != BLANK:
                    h += 1
        if h == 16:
            return (True, "tie")
        for i in range(1, 4):

            if (bord[i][1] == bord[i][2] == bord[i][3]) and bord[i][
                1
            ] != BLANK:
                return (True, turn)
            if (bord[1][i] == bord[2][i] == bord[3][i]) and bord[1][
                i
            ] != BLANK:
                return (True, turn)

        if (bord[1][1] == bord[2][2] == bord[3][3]) and bord[1][1] != BLANK:
            return (True, turn)

        if (bord[1][3] == bord[2][2] == bord[3][1]) and bord[1][3] != BLANK:
            return (True, turn)

        return (False, "h")

    @commands.command(aliases=["ttt"])
    async def tictactoe(self, ctx: commands.Context, member: discord.Member=None):
        if member == None:
            turn = ctx.author
            board = Board(3, 3, "|")
            embed = discord.Embed(
                title="TicTacToe",
                description=f"turn: `{turn.display_name}`\n```{format_board(board)}\n```",
                color=discord.Color.blurple()
            )
            msg = await ctx.send(embed=embed)
            while True:
                if turn == ctx.author:
                    inp = await ctx.bot.wait_for(
                        "message",
                        check=lambda m: m.author == turn and m.channel == ctx.channel,
                    )
                    if inp.content == "cancel":
                        return await ctx.send("Cancelled the game")
                    outp = make_move(inp.content, board, "x")
                    if outp[0]:
                        board = outp[1]
                    else:
                        await ctx.send(outp[1], delete_after=5)
                        continue
                else:
                    board = make_random_move(board)
                h = has_won(board, 'x' if turn == ctx.author else 'o')
                if h[0]:
                    return await ctx.send(
                        embed=discord.Embed(
                            color = discord.Color.blurple(),
                            title="TicTacToe",
                            description=(
                                "winner: `"
                                f"{'tie' if h[1] == 'tie' else (ctx.author.display_name if turn == ctx.author else bot.user.display_name)}`"
                                "\n"
                                f"```{format_board(board)}```"
                                "\n"
                            ),
                        )
                    )
                turn = ctx.bot.user if turn == ctx.author else ctx.author
                await msg.edit(
                    embed=discord.Embed(
                        title="TicTacToe",
                        description=f"turn: `{turn.display_name}`\n```{format_board(board)}\n```",
                        color=discord.Color.blurple()
                    )
                )
        if member.bot or member == ctx.author:
            return await ctx.send(
                f"Invalid Syntax: Can't play against {member.display_name}"
            )
        turn = ctx.author
        board = Board(3, 3, "|")
        embed = discord.Embed(
            title="TicTacToe",
            description=f"turn: `{turn.display_name}`\n```{format_board(board)}\n```",
            color=discord.Color.blurple()
        )
        msg = await ctx.send(embed=embed)
        while True:
            inp = await ctx.bot.wait_for(
                "message",
                check=lambda m: m.author == turn and m.channel == ctx.channel,
            )
            if inp.content == "cancel":
                return await ctx.send("Cancelled the game")
            outp = self.make_move(
                inp.content, board, "x" if turn == ctx.author else "o"
            )
            if outp[0]:
                board = outp[1]
            else:
                await ctx.send(outp[1])
                continue
            h = self.has_won(board, "x" if turn == ctx.author else "o")
            if h[0]:
                return await ctx.send(
                    embed=discord.Embed(
                        title="TicTacToe",
                        description=(
                            "winner: `"
                            f"{'tie' if h[1] == 'tie' else (ctx.author.display_name if h[1] == 'x' else member.display_name)}`"
                            "\n"
                            f"```{format_board(board)}```"
                            "\n"
                        ),
                    )
                )
            turn = member if turn == ctx.author else ctx.author
            await msg.edit(
                embed=discord.Embed(
                    title="TicTacToe",
                    description=f"turn: `{turn.display_name}`\n```{format_board(board)}\n```",
                )
            )
