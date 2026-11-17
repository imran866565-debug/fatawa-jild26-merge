#!/usr/bin/env python3
"""Merge Jild 26 tashreeh chunks into jild-26.json.

Re-runnable: reads every jild-26-chunk-*.json listed in the manifest,
merges in chunk order, validates (unique ids, page coverage, empty
jawab allow-list), writes jild-26.json, and updates the manifest statuses.

INPUT (verified on disk by the parent):
  11 chunk files (no splits), 268 chunk items, volume_id 34. Source
  export ~/workspace/fatawa-app/content/jild-26.json: 562 rows but
  only 561 UNIQUE pages (p. 496 has TWO rows — both belong to
  masala-265, the whole Iqamah al-Qiyamah risala; the coordinator
  verified the correct reading order: the 1,716-char row FIRST, then
  the 1,802-char row; p. 496 appears ONCE in masala-265's pages
  array). This is the Jild 16 precedent (543 rows, 542 unique pages).
  Validate the merged page union against the source export's 561
  UNIQUE pages, NOT the 562 row count. Gaps (48, nothing invented):
  pp. 12-54 (43), 139, 152, 212, 494, 583 — every gap listed in the
  manifest's source_gaps and in each chunk's missing_pages (Jild 17
  lesson), except pp. 152, 212, 494 which lie BETWEEN chunks (152
  between chunk 02 end p. 151 and chunk 03 start p. 153; 212 between
  chunk 03 end p. 211 and chunk 04 start p. 213; 494 between chunk 09
  end p. 493 and chunk 10 start p. 495) and are inside NO chunk's
  span (listed in the manifest as inter_chunk_gaps). Validate against
  the chunk items' page union (561 pages), NOT range arithmetic.

COMBINE RULES (1 case; parts ordered by min page; pages = UNION of
all parts' pages; notes = all parts' notes; start_page = min page):
  masala 31:   SAME-ID, sawal from first, jawab concatenated.
               Chunk 01 [104] (sawal 581, jawab 611) + chunk 02 [105]
               (empty sawal, jawab 380) -> [104, 105]. Sawal 581,
               jawab 991 (611 + 380). One mas'ala split across the
               chunk 01/02 boundary. Boundary clean: masala-32 starts
               after it in chunk 02; masala-64 ends p. 151.
After the combine: 268 - 1 = 267 items covering 561 unique pages.

RENAMES: NO merge-time renames. Two renames were already applied in
the chunk files and must NOT be re-applied:
  printed "mas'ala 131" on p. 433 -> 'jild26-masala-231' [433]
  (chunk 08; sequence 230 -> 232 proves 231; note recorded in the
  chunk file).
  printed "67" on p. 349 -> 'jild26-masala-167' [349] (chunk 06;
  sequence 166 -> 168 proves 167, leading 1 dropped; note recorded
  in the chunk file).
Do NOT globally normalise bare ids.

WARNINGS — the rename distinctions (checked by the coordinator
against ALL chunk files, and verified by the parent):
  A GENUINE 'jild26-masala-131' [296-298] exists in chunk 05 (a real
  mas'ala 131 in the lesson-93 sequence, sawal 2,017, jawab 1,247).
  It is a DIFFERENT item from the renamed 'jild26-masala-231' [433]
  and must be kept as-is. Do NOT confuse the two; do NOT rename it;
  do NOT merge it with masala-231. The merged file must contain BOTH
  'jild26-masala-131' [296-298] AND 'jild26-masala-231' [433] as
  separate items. (This is the Jild 24 masala-279 / Jild 25
  masala-129 lesson.)
  NO genuine 'jild26-masala-67' exists anywhere in Jild 26 — risala
  91's masail 66-72 have no separate headings (numbering jumps
  65 -> 73), verified against ALL chunk files — so the masala-167
  rename has no collision. Do NOT create a masala-67 item.

EMPTY-JAWAB ALLOW-LIST: after the combine, exactly TWO items have an
empty tashreeh_jawab: 'jild26-masala-22' [94] (sawal 203 chars, jawab
EMPTY) and 'jild26-masala-24' [95] (sawal EMPTY, jawab EMPTY). Both
are genuine, verified by the coordinator from the source: masala-22
— only the question's opening line exists; division table absent, no
jawab before masala-23 starts on the same page; masala-24 — ONLY the
heading "mas'ala 24: 30 Safar 1311H", no question and no answer. The
merge script allow-lists exactly these two items. All other items
must have non-empty jawab (the split-head empty jawab — masala-31
[105] — is resolved by the combine). Empty sawal after merge:
exactly 6 (pesh-lafz, masala-24, risala-intro, masala-251,
masala-268, masala-319 — all by design).

DO-NOT-COMBINES: NO combine for the 303/304 boundary: masala-133
stays pages [300-303]; its jawab's final line sits at the top of
p. 304 and is already covered in chunk 05's tashreeh (recorded in
its notes); chunk 06 created no masala-133 tail item. Do NOT create
a phantom half. NO combine for the 258/259 boundary: masala-97 stays
pages [245-258]; its closing hamd line ("wa bi-rabbina nakhuss
al-hamd kullah...") spills onto the top of p. 259 (verified by the
coordinator from the source text of p. 259) and is recorded in
masala-97's notes; chunk 05's masala-98 starts on p. 259. Do NOT
create a masala-97 tail item. Masala-89 is a SEPARATE item
(coordinator's decision, verified from source): p. 207 is only 177
chars (new case: Aasudah took Muhammad Hussain's cash/household
goods beyond her share and left with 2-year-old Ali Hussain, missing
12 years); p. 208 gives the ruling (70 shares in trust till age 70,
mas'alah al-zafar) before masala-90's heading starts mid-page. New
persons, new topic, sequence 88 -> 90 — it IS masala-89. Do NOT fold
it into masala-88. P. 496: both rows belong to masala-265 (the whole
Iqamah al-Qiyamah risala [495-551], sawal 485, jawab 34,125); p. 496
appears once in its pages array. Masala-264 ends on p. 493, so no
preceding item could end on p. 496. Whole-risala single items (NOT
combines — already single): masala-258 = whole al-Samsam risala
[467-487] (jawab 30,261); masala-265 = whole Iqamah al-Qiyamah
risala [495-551]; masala-315 = whole Kashf Haqa'iq risala [595-604];
masala-204 [374-394] (21 pp.) closes lesson 93, no separate khatima.
Combined headings kept as single items (first number's id): 36 wa 37
-> masala-36 [112-118]; 112 ta 127 -> masala-112 [287-292] (sawal
2,609, jawab 3,281); 147/148 -> masala-147 [331-332]; 149-152 ->
masala-149 [332-337]; 157/158 -> masala-157 [343-344]; 160-162 ->
masala-160 [344-345]; 169-173 -> masala-169 [350-352]; 175,176 ->
masala-175 [353-354]; 194-196 -> masala-194 [367-368]; 206,207 ->
masala-206 [396]; 234-241 -> masala-234 [434-435]; 253 ta 255 ->
masala-253-255 [460-463]; 270,271 -> masala-270; 278,279 ->
masala-278; 281 wa 282 -> masala-281; 289 wa 290 -> masala-289;
293 wa 294 -> masala-293; 295 wa 296 -> masala-295; 299 wa 300 ->
masala-299; 301 ta 304 -> masala-301; 305 ta 307 -> masala-305;
323 wa 324 -> masala-323. Masala-65 (risala 91, al-Maqsad al-Nafi')
holds ALL 8 sub-questions — masail 66-72 have NO separate headings
(numbering jumps 65 -> 73). No genuine 'jild26-masala-67' exists
anywhere. Shared pages by design (one mas'ala's tail + the next
one's start on the same page): 221, 231, 239, 245 (chunk 04) and
others across chunks — page union still exactly 561. Volume ends
p. 613 with the closing note "26th jild Kitab al-Fara'id se shuru ho
kar Kitab al-Shatta ke hissa awwal par ikhtitam pazir hui, in sha
Allah al-Aziz 27th jild Kitab al-Shatta hissa doom se shuru hogi."
recorded in masala-325's notes. No separate khatima item. Last item
'jild26-masala-325' [612-613]. PUA-garbled words flagged in notes
only, never reconstructed: pp. 567, 586, 592, 598 (chunk 11).
Image-only / missing-text pages (nothing invented): p. 243 (image
page, four jaddat diagrams of masala-96); p. 336 (image-only shajra
page inside masala-149); pp. 320-323, 324, 325, 328-329 (division
tables as images, figures not in text); p. 422 (garbled table in
masala-223); p. 426 ("Start Ki Image Nahi Hai" in masala-223).

SORT: merged items are sorted by start_page for the final file.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# result id -> list of selectors, in page order.
# Selector forms:
#   ('id', sid)            — every item with this id (1 or 2 halves)
#   ('id_start', sid, sp)  — the item with this id starting at page sp
COMBINES = {
    'jild26-masala-31': [
        ('id', 'jild26-masala-31'),
    ],
}

# Sawal handling per combined id (default: sawal from the first part,
# sorted by min page). The single combine in this volume is
# sawal-from-first — there is NO concatenation case.
SAWAL_RULES = {}

# No merge-time renames in this volume. The two renames (printed 131
# p. 433 -> masala-231; printed 67 p. 349 -> masala-167) were already
# applied in the chunk files and are asserted present below. Kept
# empty deliberately.
RENAMES = {}

# Applied-in-chunk renames (already in the chunk files — must exist
# after merging, never re-applied).
RENAMED_IN_CHUNK = ['jild26-masala-231', 'jild26-masala-167']

# Expected pages for every combined item (spot-check anchors).
EXPECTED_COMBINED_PAGES = {
    'jild26-masala-31': [104, 105],
}

# Expected sawal/jawab char counts for every combined item.
# masala-31 jawab: 611 + 380 = 991
EXPECTED_COMBINED_TEXT = {
    'jild26-masala-31': (581, 991),
}

# No cross-id combine in this volume, so no absorbed ids.
ABSORBED = []

# The only items allowed to keep an empty sawal after merging
# (all by design).
EMPTY_SAWAL_ALLOWED = {
    'jild26-pesh-lafz',
    'jild26-masala-24',
    'jild26-risala-intro',
    'jild26-masala-251',
    'jild26-masala-268',
    'jild26-masala-319',
}

# The ONLY items allowed to keep an empty tashreeh_jawab after
# merging: BOTH genuine, verified by the coordinator from the source.
# masala-22 [94]: only the question's opening line exists; division
# table absent, no jawab before masala-23 starts on the same page.
# masala-24 [95]: ONLY the heading "mas'ala 24: 30 Safar 1311H" —
# no question and no answer. Every other item must have a non-empty
# jawab (the split-head empty jawab — masala-31 [105] — is resolved
# by the combine).
EMPTY_JAWAB_ALLOWED = {'jild26-masala-22', 'jild26-masala-24'}

# BOTH masala-131 and masala-231 must exist as SEPARATE items (see
# WARNING in the docstring above): the genuine masala-131 [296-298]
# and the renamed masala-231 [433].
BOTH_131_AND_231 = {
    'jild26-masala-131': [296, 297, 298],
    'jild26-masala-231': [433],
}

# NO genuine masala-67 exists anywhere in Jild 26 (risala 91's
# masail 66-72 have no separate headings; numbering jumps 65 -> 73).
NO_MASALA_67 = 'jild26-masala-67'


def combine_parts(result_id, parts):
    parts = sorted(parts, key=lambda it: min(it['pages']))
    first = parts[0]
    rule = SAWAL_RULES.get(result_id)
    if rule and rule[0] == 'concat':
        sawal = ''.join((parts[i].get('tashreeh_sawal', '') or '')
                        for i in rule[1])
    elif rule and rule[0] == 'from':
        sawal = parts[rule[1]].get('tashreeh_sawal', '') or ''
    else:
        sawal = first.get('tashreeh_sawal', '') or ''
    title = first.get('title') or ''
    combined = {
        'id': result_id,
        'title': title,
        'volume_id': 34,
        'pages': sorted(set().union(*[set(p['pages']) for p in parts])),
        'start_page': min(min(p['pages']) for p in parts),
        'tashreeh_sawal': sawal,
        'tashreeh_jawab': ''.join((p.get('tashreeh_jawab', '') or '') for p in parts),
        'notes': [n for p in parts for n in (p.get('notes') or [])],
    }
    return combined


def select_parts(all_items, selectors):
    """Resolve selectors to the matching items (each used at most once)."""
    parts = []
    used = set()
    for sel in selectors:
        if sel[0] == 'id':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and id(it) not in used]
        elif sel[0] == 'id_start':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and it['start_page'] == sel[2]
                    and id(it) not in used]
        else:
            raise ValueError(f'unknown selector {sel}')
        assert hits, f'no items matched selector {sel}'
        for it in hits:
            used.add(id(it))
        parts.extend(hits)
    return parts


def run_merge(manifest_path, base, write=False):
    manifest = json.load(open(manifest_path, encoding='utf-8'))
    all_items = []
    merged_chunks = []
    for entry in manifest['chunks']:
        nn = entry['chunk']
        if entry.get('status') == 'split-halves':
            print(f'chunk {nn}: split-halves placeholder — halves are separate entries, skipping')
            continue
        # A chunk may be one file ("file") or split halves ("files").
        file_list = entry.get('files') or [entry['file']]
        items = []
        for fname in file_list:
            path = os.path.join(base, fname)
            if not os.path.exists(path):
                print(f'chunk {nn}: {fname} not yet written')
                continue
            try:
                d = json.load(open(path, encoding='utf-8'))
            except json.JSONDecodeError as e:
                # File may still be streaming from its translator; skip it
                # for now instead of crashing the whole merge.
                print(f'chunk {nn}: {fname} not valid JSON yet ({e}) — skipping for now')
                continue
            items.extend(d['masail'])
        if not items:
            print(f'chunk {nn}: no items loaded — skipping')
            continue
        # Normalize: some translators omit start_page; derive it from pages.
        for it in items:
            if 'start_page' not in it:
                assert it.get('pages'), f'chunk {nn} item {it.get("id")} has no pages'
                it['start_page'] = it['pages'][0]
                print(f'chunk {nn}: derived start_page={it["start_page"]} for {it["id"]}')
            assert it['start_page'] == min(it['pages']), \
                f'chunk {nn} item {it["id"]}: start_page != first page'
            it['_src_file'] = file_list[0]
        all_items.extend(items)
        merged_chunks.append(nn)
        entry['status'] = 'merged'
        print(f'chunk {nn}: {len(items)} items merged')
    print(f'items before combines: {len(all_items)}')
    assert len(all_items) == 268, f'expected 268 chunk items, got {len(all_items)}'
    # COMBINE the 1 case (one mas'ala split across chunks).
    for result_id, selectors in COMBINES.items():
        parts = select_parts(all_items, selectors)
        combined = combine_parts(result_id, parts)
        assert combined['pages'] == EXPECTED_COMBINED_PAGES[result_id], \
            f'{result_id}: pages {combined["pages"]} != expected {EXPECTED_COMBINED_PAGES[result_id]}'
        exp_sawal, exp_jawab = EXPECTED_COMBINED_TEXT[result_id]
        assert len(combined['tashreeh_sawal']) == exp_sawal, \
            f'{result_id}: sawal {len(combined["tashreeh_sawal"])} chars != expected {exp_sawal}'
        assert len(combined['tashreeh_jawab']) == exp_jawab, \
            f'{result_id}: jawab {len(combined["tashreeh_jawab"])} chars != expected {exp_jawab}'
        assert combined['tashreeh_jawab'], f'{result_id}: combined jawab is empty!'
        assert combined['tashreeh_sawal'], f'{result_id}: combined sawal is empty!'
        assert combined['start_page'] == min(combined['pages']), f'{result_id}: start_page != min(pages)'
        used_ids = set(id(p) for p in parts)
        all_items = [it for it in all_items if id(it) not in used_ids]
        all_items.append(combined)
        print(f'COMBINED {result_id}: {len(parts)} parts, pages {combined["pages"][0]}-{combined["pages"][-1]} '
              f'({len(combined["pages"])} pages), sawal {len(combined["tashreeh_sawal"])} chars, '
              f'jawab {len(combined["tashreeh_jawab"])} chars, notes {len(combined["notes"])}')
    # RENAMES: none to apply as a separate step (no merge-time renames
    # in this volume; the applied-in-chunk renames are already in the
    # chunk files and are asserted present below).
    for old_id, new_id in RENAMES.items():
        assert not any(it['id'] == new_id for it in all_items), \
            f'rename target {new_id} already exists!'
        hits = [it for it in all_items if it['id'] == old_id]
        assert len(hits) == 1, f'rename source {old_id}: expected exactly 1 item, found {len(hits)}'
        hits[0]['id'] = new_id
        print(f'RENAMED {old_id} -> {new_id} (pages {hits[0]["pages"][0]}-{hits[0]["pages"][-1]})')
    # Verify absorbed ids are gone (none in this volume).
    for sid in ABSORBED:
        assert not any(it['id'] == sid for it in all_items), \
            f'absorbed id {sid} must not exist after combining!'
    print(f'absorbed ids gone: {len(ABSORBED)}')
    # Verify applied-in-chunk renames exist (already in the chunk files).
    for sid in RENAMED_IN_CHUNK:
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'applied-in-chunk id {sid}: expected exactly 1 item, found {len(hits)}'
    print(f'applied-in-chunk renames present: {RENAMED_IN_CHUNK}')
    # Verify BOTH masala-131 and masala-231 exist as separate items
    # with their exact pages (the Jild 24 masala-279 / Jild 25
    # masala-129 lesson — do NOT treat 231 as a duplicate of the
    # genuine 131).
    for sid, exp_pages in BOTH_131_AND_231.items():
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'{sid}: expected exactly 1 item, found {len(hits)}'
        assert hits[0]['pages'] == exp_pages, \
            f'{sid}: pages {hits[0]["pages"]} != expected {exp_pages}'
    print(f'both 131 and 231 present as separate items: {BOTH_131_AND_231}')
    # NO genuine masala-67 may exist anywhere in the volume.
    assert not any(it['id'] == NO_MASALA_67 for it in all_items), \
        f'{NO_MASALA_67} must NOT exist (no genuine masala-67 in Jild 26)'
    print(f'no {NO_MASALA_67} present (as expected)')
    ids = [it['id'] for it in all_items]
    assert len(ids) == len(set(ids)), f'STILL DUPLICATE IDS: {[i for i in ids if ids.count(i) > 1]}'
    empty = [it['id'] for it in all_items if not it.get('tashreeh_jawab')]
    assert set(empty) == EMPTY_JAWAB_ALLOWED, \
        f'EMPTY JAWAB mismatch: {sorted(empty)} != {sorted(EMPTY_JAWAB_ALLOWED)}'
    print(f'empty jawab (allow-listed only): {sorted(empty)}')
    empty_sawal = [it['id'] for it in all_items if not it.get('tashreeh_sawal')]
    assert set(empty_sawal) == EMPTY_SAWAL_ALLOWED, \
        f'EMPTY SAWAL mismatch: {sorted(empty_sawal)} != {sorted(EMPTY_SAWAL_ALLOWED)}'
    print(f'empty sawal (by design only): {sorted(empty_sawal)}')
    pages = set()
    for it in all_items:
        pages.update(it['pages'])
    # PRIMARY coverage check (Jild 17 lesson): validate against the 561
    # unique pages directly, not against a range-minus-gaps computation
    # (pp. 152, 212, 494 are inter-chunk gaps inside NO chunk's span).
    assert len(pages) == 561, f'expected 561 unique pages, got {len(pages)}'
    assert min(pages) == 5 and max(pages) == 613, \
        f'page span {min(pages)}-{max(pages)} != 5-613'
    # Secondary cross-check: per-chunk page count and item count must
    # equal the manifest's values for that chunk. (This manifest uses
    # 'pages' for the unique-page COUNT and 'items' for the item count;
    # combined items carry pages from several chunks, so per-chunk
    # attribution must come from the raw file, not from the merged items.)
    for entry in manifest['chunks']:
        if entry['chunk'] in merged_chunks:
            d = json.load(open(os.path.join(base, entry['file']), encoding='utf-8'))
            raw_pages = set()
            for it in d['masail']:
                raw_pages.update(it['pages'])
            assert len(raw_pages) == entry['pages'], \
                f'chunk {entry["chunk"]}: {len(raw_pages)} unique pages != manifest {entry["pages"]}'
            assert len(d['masail']) == entry['items'], \
                f'chunk {entry["chunk"]}: {len(d["masail"])} items != manifest {entry["items"]}'
    print(f'total items: {len(all_items)} | pages covered: {len(pages)}')
    assert len(all_items) == 267, f'expected 267 items after combines, got {len(all_items)}'
    # sort by start_page for the final file
    all_items.sort(key=lambda it: it['start_page'])
    for it in all_items:
        it.pop('_src_file', None)
    if write:
        with open(os.path.join(base, 'jild-26.json'), 'w', encoding='utf-8') as f:
            json.dump({'masail': all_items}, f, ensure_ascii=False, indent=1)
        with open(os.path.join(base, 'chunks-manifest-jild26.json'), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f'WROTE jild-26.json: {len(all_items)} items, {len(pages)} pages, chunks merged: {merged_chunks}')
    return all_items, pages, merged_chunks


def main():
    manifest_path = os.path.join(BASE, 'chunks-manifest-jild26.json')
    run_merge(manifest_path, BASE, write=True)


if __name__ == '__main__':
    main()
