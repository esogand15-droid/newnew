from pathlib import Path
p=Path('/home/user/work/render/render.py')
s=p.read_text(encoding='utf-8')
old=''' <div class="callout quran"><b class="quran-title">اسراء/۳۱ | مضمونِ چاپ‌شده در منبع</b>
   <p class="quran-meaning"><b>معنیِ نقل‌شده:</b> فرزندانتان را از بیم تنگ‌دستی نکشید؛ خدا به آنان و شما روزی می‌دهد؛ کشتن آنان گناهی بزرگ است.</p>
   <p class="quran-note"><b>یادداشت تطبیقی:</b> در نسخهٔ منبع، کنار این ترجمه عبارت عربیِ کوتاه‌شده‌ای آمده که با ترجمهٔ فارسیِ همان منبع کاملاً هم‌خوان نیست. برای جلوگیری از تثبیت نقل نادقیق، این کادر معنای چاپ‌شده را حفظ می‌کند و آن عبارت را متن کامل آیه معرفی نمی‌کند.</p>
 </div>'''
new=''' <div class="callout quran"><b class="quran-title">آیهٔ کامل | اسراء/۳۱</b>
   <p class="quran-ar" dir="rtl" lang="ar">وَلَا تَقْتُلُوا أَوْلَادَكُمْ خَشْيَةَ إِمْلَاقٍ ۖ نَحْنُ نَرْزُقُهُمْ وَإِيَّاكُمْ ۚ إِنَّ قَتْلَهُمْ كَانَ خِطْئًا كَبِيرًا</p>
   <p class="quran-meaning"><b>معنی:</b> فرزندانتان را از بیم تنگ‌دستی نکشید؛ ما به آنان و شما روزی می‌دهیم؛ کشتن آنان گناهی بزرگ است.</p>
   <p class="quran-note"><b>یادداشت تطبیقی:</b> در PDF منبع، متن عربیِ این موضع با ترجمهٔ فارسی و ارجاع «اسراء/۳۱» هم‌خوانی کامل ندارد؛ این کادر متن عربی و شماره را با قرآن تطبیق می‌دهد و ترجمهٔ فارسیِ منبع را نگه می‌دارد.</p>
 </div>'''
assert s.count(old)==1
s=s.replace(old,new,1)
old=''' <div class="callout quran"><b class="quran-title">بخشِ مورد بحث | اسراء/۶۴</b>
   <p class="quran-ar" dir="rtl" lang="ar">وَشَارِكْهُمْ فِي الْأَمْوَالِ وَالْأَوْلَادِ</p>
   <p class="quran-meaning"><b>معنیِ عبارت:</b> و در اموال و فرزندانشان مشارکت کن.</p>
   <p class="quran-note"><b>پیوند با مبحث:</b> توضیح منبع، مشارکت را در پیوند با مالِ به‌دست‌آمده از راه حرام یا معصیت می‌داند و از همین‌جا رعایت حلال و حرام در کسب‌وکار را نتیجه می‌گیرد. <b>توضیح ارجاع:</b> صفحهٔ ۱۰۸ منبع برای نقلِ بلند «اسراء/۶۷» چاپ کرده و در ادامه از ذیل آیهٔ ۶۶ نام می‌برد؛ پس ارجاع‌های آن موضع یکدست نیستند.</p>
 </div>'''
new=''' <div class="callout quran"><b class="quran-title">آیهٔ کامل | اسراء/۶۴</b>
   <p class="quran-ar" dir="rtl" lang="ar">وَاسْتَفْزِزْ مَنِ اسْتَطَعْتَ مِنْهُمْ بِصَوْتِكَ وَأَجْلِبْ عَلَيْهِمْ بِخَيْلِكَ وَرَجِلِكَ وَشَارِكْهُمْ فِي الْأَمْوَالِ وَالْأَوْلَادِ وَعِدْهُمْ ۚ وَمَا يَعِدُهُمُ الشَّيْطَانُ إِلَّا غُرُورًا</p>
   <p class="quran-meaning"><b>معنی:</b> هرکس از آنان را توانستی با ندایت به لغزش انداز و سواره‌نظام و پیاده‌نظامت را بر آنان بسیج کن؛ در اموال و فرزندانشان شریک شو و به آنان وعده بده؛ وعدهٔ شیطان جز فریب نیست.</p>
   <p class="quran-note"><b>پیوند با مبحث:</b> توضیح منبع، عبارتِ مشارکت را در پیوند با مالِ به‌دست‌آمده از راه حرام یا معصیت می‌داند و از همین‌جا رعایت حلال و حرام در کسب‌وکار را نتیجه می‌گیرد. <b>یادداشت تطبیقی:</b> صفحهٔ ۱۰۸ منبع برای نقلِ بلند «اسراء/۶۷» چاپ کرده و در ادامه از ذیل آیهٔ ۶۶ نام می‌برد؛ این کادر متن و شماره را با آیهٔ ۶۴ تطبیق می‌دهد.</p>
 </div>'''
assert s.count(old)==1
s=s.replace(old,new,1)
# Make the scope comment accurately describe the two source-verified Arabic corrections.
s=s.replace('''# Content pages are authored from the supplied Markdown and checked against the
# source PDF linked in the prompt. Uncertain OCR-only details are not presented
# as verified facts.''','''# Content pages are authored from the supplied source PDF. Quranic text and
# citations are checked against the source; the two discrepant Isra references
# are transparently corrected against Quran.com at the user's request.''')
p.write_text(s,encoding='utf-8')
print('Corrected both Isra boxes in',p)
