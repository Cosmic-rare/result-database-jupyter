# 各Builderの評価

## score

- builder1: 精度1.0
- builder2: 精度1.0
- builder3: 精度1.0
- builder4: 精度1.0
- builder5: 7を/と誤認
- builder6: 7を/と誤認

## title

- builder1: 空っぽ 特に空白対策が必須
- builder2: 空っぽ 特に空白対策が必須
- builder3: 0.8923076923076922 空白対策が必須

## difficult

- builder1: 0.8730769230769231 空白対策が必須 一個だけ完璧があった
- builder2: 0.8875 空白対策が必須 二個だけ完璧があった
- builder3: 0.7049535603715171 空白対策が必須 ジャケットとかを誤認している
- builder4: 0.724561403508772 空白対策が必須 ジャケットとかを誤認している

## judge

- builder1: 0.95 空っぽ2
- builder2: 0.75 空っぽ1 0を6と誤認 空っぽ3
- builder3: 0.95 空っぽ2
- builder4: 0.75 空っぽ1 0を6と誤認 空っぽ2 空っぽ3
- builder5: 0.95 謎文字として認識
- builder6: 0.95 0を6と誤認

- builder1 or builder3をメインにする
- 空っぽの時、数字のみのbuilder5を使う
- 空っぽの時、数字のみのbuilder6を使う
- それも空っぽの時、builder2 -> builder4 -> Error
