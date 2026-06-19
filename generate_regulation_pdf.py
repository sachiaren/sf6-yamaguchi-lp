# -*- coding: utf-8 -*-
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUTPUT = Path("regulation_latest.pdf")
FONT_REGULAR = r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
FONT_BOLD = r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"

pdfmetrics.registerFont(TTFont("EventGothic", FONT_REGULAR, subfontIndex=0))
pdfmetrics.registerFont(TTFont("EventGothic-Bold", FONT_BOLD, subfontIndex=0))

NAVY = colors.HexColor("#07143f")
ORANGE = colors.HexColor("#ff6a00")
LIGHT = colors.HexColor("#eef2fb")
LINE = colors.HexColor("#dfe6f2")
TEXT = colors.HexColor("#172033")

base = ParagraphStyle(
    "Base",
    fontName="EventGothic",
    fontSize=9.5,
    leading=15,
    wordWrap="CJK",
    textColor=TEXT,
    spaceAfter=5,
)

title = ParagraphStyle(
    "Title",
    parent=base,
    fontName="EventGothic-Bold",
    fontSize=22,
    leading=29,
    alignment=TA_CENTER,
    textColor=NAVY,
    spaceAfter=8,
)

subtitle = ParagraphStyle(
    "Subtitle",
    parent=base,
    fontName="EventGothic-Bold",
    fontSize=12,
    leading=18,
    alignment=TA_CENTER,
    textColor=ORANGE,
    spaceAfter=12,
)

section = ParagraphStyle(
    "Section",
    parent=base,
    fontName="EventGothic-Bold",
    fontSize=14,
    leading=20,
    textColor=NAVY,
    spaceBefore=11,
    spaceAfter=7,
)

strong = ParagraphStyle(
    "Strong",
    parent=base,
    fontName="EventGothic-Bold",
    fontSize=10,
    leading=15,
    textColor=NAVY,
)


def p(text, style=base):
    return Paragraph(text.replace("\n", "<br/>"), style)


def h(text):
    return p(text, section)


def bullet(items):
    return [p("・" + item) for item in items]


def info_table(rows, widths=(38 * mm, 122 * mm)):
    data = [[p(label, strong), p(value)] for label, value in rows]
    table = Table(data, colWidths=list(widths), hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), LIGHT),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def two_column_cards(left_title, left_items, right_title, right_items):
    left = [p(left_title, strong)] + bullet(left_items)
    right = [p(right_title, strong)] + bullet(right_items)
    table = Table([[left, right]], colWidths=[80 * mm, 80 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, ORANGE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("EventGothic", 7.5)
    canvas.setFillColor(colors.HexColor("#4d5670"))
    canvas.drawString(15 * mm, 10 * mm, "STREET FIGHTER 6 山口県選手権 大会レギュレーション")
    canvas.drawRightString(195 * mm, 10 * mm, str(doc.page))
    canvas.restoreState()


story = [
    p("STREET FIGHTER 6<br/>山口県選手権", title),
    p("大会レギュレーション / 最新版", subtitle),
    p(
        "本資料は、2026年7月20日（月・祝）に湯田温泉こんこんパークで開催する"
        "「STREET FIGHTER 6 山口県選手権」の大会概要、参加条件、進行ルール、注意事項をまとめたものです。"
    ),
]

story += [
    h("1. 開催概要"),
    info_table(
        [
            ("大会名", "STREET FIGHTER 6 山口県選手権"),
            ("開催日", "2026年7月20日（月・祝）"),
            ("開催時間", "10:00〜16:00"),
            ("会場", "湯田温泉こんこんパーク"),
            ("住所", "山口市湯田温泉5丁目2番15号"),
            ("参加費", "1,000円（大会参加料）"),
            ("申込期間", "2026年6月1日〜7月10日まで"),
            ("応募方法", "トナメルより応募"),
            ("受付", "定員に達し次第終了"),
        ]
    ),
    Spacer(1, 4 * mm),
    p("山口県内外を問わず、どなたでも参加できます。場内には無料対戦コーナーも設置予定です。"),
    h("2. トーナメント部門"),
    two_column_cards(
        "マスターズトーナメント",
        ["対象：ランク マスター以上", "定員：最大64人", "応募時点のランクを基準に応募してください。"],
        "チャレンジトーナメント",
        ["対象：ランク マスター未満", "ランクマッチ未プレイの方も参加可能", "定員：最大32人"],
    ),
    Spacer(1, 4 * mm),
]

story += bullet(
    [
        "過去に1キャラクターでもマスターランクに到達したことがある方は、現在使用するキャラクターがマスター未満であってもマスターズトーナメントへ応募してください。",
        "チャレンジ応募後にマスターへ昇格した場合は、WhiteFox公式XのDMでご相談ください。",
        "虚偽申告が判明した場合は、出場不可となる可能性があります。",
    ]
)

story += [
    h("3. トーナメント表"),
    *bullet(
        [
            "トーナメント表は2026年7月12日以降にWhiteFox公式XおよびHPにて公開予定です。",
            "公開時には、トナメルに登録されたプレイヤー名 / エントリーネームを掲載します。",
        ]
    ),
    h("4. 大会形式"),
    *bullet(
        [
            "本大会はダブルエリミネーション形式で実施します。",
            "各マッチは原則2ゲーム先取（BO3）です。",
            "TOP4以降は3ゲーム先取（BO5）です。",
            "マスターズトーナメントは8つのブロックに分かれてダブルエリミネーションで代表を決定し、決勝トーナメントもダブルエリミネーションで対戦します。",
            "チャレンジトーナメントは4つのブロックに分かれてダブルエリミネーションで代表を決定し、決勝トーナメントもダブルエリミネーションで対戦します。",
            "TOP4以降は両トーナメントとも大型ビジョン前のステージ台で進行予定です。",
            "参加人数や当日の状況により、形式・進行方法・終了時間を変更する場合があります。",
        ]
    ),
    p("BO5対象マッチ", strong),
    *bullet(
        [
            "ウィナーズファイナル",
            "ルーザーズセミファイナル",
            "ルーザーズファイナル",
            "グランドファイナル",
            "グランドファイナルリセット（発生時のみ）",
        ]
    ),
    h("5. タイムテーブル"),
    info_table(
        [
            ("9:00〜9:45", "受付"),
            ("9:45〜9:55", "開会説明・ルール説明"),
            ("10:00〜12:20", "大会進行 / TOP4決定まで / BO3"),
            ("12:30〜16:00", "TOP4以降 / BO5 / 両トーナメントともステージ台1台で進行予定"),
        ],
        widths=(42 * mm, 118 * mm),
    ),
    h("6. 使用環境 / ゲーム内設定"),
    *bullet(
        [
            "使用ハード：PC",
            "使用バージョン：大会当日時点で運営が指定するバージョン",
            "コントローラー：マイアケコン・コントローラーを各自持参してください。",
            "持ち込み機材の接続不良・動作不良は原則本人責任です。",
            "ラウンド数：2ラウンド先取",
            "ラウンドタイム：99カウント",
            "ステージ：ランダム",
            "実況設定：OFF",
            "ハンディキャップ：なし",
            "その他設定：運営指定の標準設定",
        ]
    ),
    h("7. キャラクター・操作タイプ・ボタン設定"),
    *bullet(
        [
            "1マッチ目のキャラクター / 操作タイプ選択は自由です。",
            "マッチ開始後のキャラクター変更および操作タイプ変更はできません。",
            "同一マッチ内では最初に選択したキャラクター・操作タイプで進行します。",
            "次のマッチでは改めて選択可能です。",
            "マッチ開始前にキャラクター、操作タイプ、ボタン設定を必ず確認してください。",
            "マッチ開始後の設定ミスは原則そのまま続行し、結果は有効です。",
            "ポーズ・中断時は状況によりラウンド敗北、ゲーム敗北、マッチ敗北の場合があります。",
            "最終判断は運営が行います。",
        ]
    ),
    h("8. 呼び出し・遅刻・トラブル対応"),
    *bullet(
        [
            "呼び出しは会場アナウンスで行います。",
            "参加者は自身のマッチ状況を随時確認してください。",
            "呼び出し後は速やかに指定台へ移動してください。",
            "一定時間来ない場合は、運営判断で不戦敗となる場合があります。",
            "マッチ中のトラブル時は両選手とも操作を止め、速やかにスタッフへ申告してください。",
            "運営側機材トラブルの場合は、運営判断で再開、再マッチ、結果有効などを決定します。",
            "トラブル後も続行した場合は、原則その結果を有効とします。",
        ]
    ),
    h("9. アクセス・駐車場"),
    info_table(
        [
            ("会場", "湯田温泉こんこんパーク"),
            ("住所", "山口市湯田温泉5丁目2番15号"),
            ("電車", "JR山口線 湯田温泉駅から徒歩10分"),
            ("高速道路", "小郡ICから約15分"),
            ("施設駐車場", "50台有料。1時間無料、それ以降1時間100円"),
            ("施設利用", "施設内で1,000円利用すると駐車料金が1時間無料"),
            ("大会参加者", "大会参加者は1時間無料"),
            ("満車時", "近隣有料駐車場をご利用ください。"),
        ]
    ),
    h("10. 撮影・喫煙・飲食"),
    *bullet(
        [
            "写真撮影は可能です。SNS投稿時は他参加者や来場者の映り込みに配慮してください。",
            "参加者・来場者による動画撮影およびライブ配信は禁止です。",
            "イベント当日の様子は、運営による記録・広報用として写真や動画を撮影し、SNSやホームページ等で発信する場合があります。",
            "館内全面禁煙です。施設外の喫煙所をご利用ください。",
            "会場内は密閉できる蓋付き飲料のみ持ち込み可能です。",
            "イベント会場内での食事はできません。",
            "飲酒しての来場は禁止です。",
        ]
    ),
    h("11. 問い合わせ / Link"),
    info_table(
        [
            ("X（WhiteFox）", "https://x.com/WhiteFox240801"),
            ("メール", "mequest.sachiaren@gmail.com"),
            ("施設HP", "https://konkon-park.com/"),
            ("やまぐちeスポーツ協会", "https://yamaguchi-esports.com/"),
            ("トナメル", "https://tonamel.com/competition/xcvye"),
        ]
    ),
    h("12. 権利表記"),
    p("本大会は株式会社カプコンの許諾を得て開催するユーザー主催大会です。公式大会ではありません。", strong),
    p("©CAPCOM", strong),
]

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=18 * mm,
    leftMargin=18 * mm,
    topMargin=18 * mm,
    bottomMargin=18 * mm,
    title="STREET FIGHTER 6 山口県選手権 大会レギュレーション",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT.resolve())
print(OUTPUT.stat().st_size)
