# superbill rules

Run these rules in order. An error stops claim preparation. A warning does not
change the superbill and the person decides whether to ask for confirmation.
Every failed rule uses the exact fix-list wording below. Never propose or make a
replacement value.

1. SB-01 | error | Check that the client name and identity date are present. | Fix list: "Please send a corrected superbill that includes the client's name and identity date exactly as shown in your records."
2. SB-02 | error | Check that practice name, practice address, practice phone, provider name, and provider credentials are present. | Fix list: "Please send a corrected superbill that includes the practice name, practice address, practice phone, provider name, and provider credentials exactly as shown in your records."
3. SB-03 | error | Check that provider license number and license state are present. | Fix list: "Please send a corrected superbill that includes the provider license number and license state exactly as shown in your records."
4. SB-04 | error | Check that the NPI is present and has exactly ten digits. | Fix list: "Please check the NPI against your records and send a corrected superbill with the exact 10-digit NPI."
5. SB-05 | error | Check the NPI check digit with the CMS Luhn method in `codes.md`. | Fix list: "Please check the NPI against your records and send a corrected superbill with the exact NPI if your record shows a correction is required."
6. SB-06 | error | Check that the practice Tax ID is present and has exactly nine digits. | Fix list: "Please check the practice Tax ID against your billing records and send a corrected superbill with the exact 9-digit Tax ID. Never send a client's number."
7. SB-07 | error | Check that every session has at least one diagnosis code in one of the two ICD-10 shapes in `codes.md`. | Fix list: "Please check the diagnosis code against the original clinical record and send a corrected superbill with the exact therapist-recorded code."
8. SB-08 | error | Check that no diagnosis code matches the U00 fabricated-code guard in `codes.md`. | Fix list: "Please check the diagnosis code against the original clinical record and replace the placeholder only with the exact therapist-recorded diagnosis code."
9. SB-09 | error | Check that at least one numbered Session block is present. | Fix list: "Please send a corrected superbill that includes at least one service-line block for the session in your records."
10. SB-10 | error | Check that each date of service is a real ISO date and is not after today. | Fix list: "Please check the date of service against your records and send a corrected superbill with the exact date in YYYY-MM-DD form."
11. SB-11 | error | Check that each CPT code has exactly five digits. | Fix list: "Please check the CPT code against the original clinical record and send a corrected superbill with the exact 5-digit code."
12. SB-12 | error | Check that each CPT code is in the psychotherapy set in `codes.md`. | Fix list: "Please check the CPT code against the original clinical record and send a corrected superbill with the exact therapist-recorded code."
13. SB-13 | error | Check that each place of service is in the mental health set in `codes.md`. | Fix list: "Please check the place of service against the encounter record and send a corrected superbill with the exact 2-digit code."
14. SB-14 | error | Check that modifier 95 appears only with telehealth place of service 02 or 10. | Fix list: "Please check the place of service and modifier against the encounter record and the insurer's own policy, then send a corrected superbill if your records show a correction is required."
15. SB-15 | error | Check that units are a positive whole number. | Fix list: "Please check the units against the original clinical record and send a corrected superbill with the exact positive whole number."
16. SB-16 | error | Check that every charge is a positive number. | Fix list: "Please check the charge against your billing records and send a corrected superbill with the exact positive amount."
17. SB-17 | error | Check that every amount paid is a positive number. | Fix list: "Please check the amount paid against your billing records and send a corrected superbill with the exact positive amount."
18. SB-18 | error | Check that every session has a diagnosis pointer. | Fix list: "Please check the diagnosis pointer against the original clinical record and send a corrected superbill with the exact pointer."
19. SB-19 | error | Check that total charge is present and is a positive number. | Fix list: "Please check the total charge against your billing records and send a corrected superbill with the exact positive total."
20. SB-20 | error | Check that total charge equals the sum of the service-line charges to the cent. | Fix list: "Please reconcile the stated total charge with the service-line charges in your billing records and send a corrected superbill with the exact recorded amounts."
21. SB-21 | error | Check that total paid is present and is a positive number. | Fix list: "Please check the total paid against your billing records and send a corrected superbill with the exact positive total."
22. SB-22 | warning | Check whether a CPT code is 90846, 90847, or 90853, the non-individual set from the input. | Fix list: "Please confirm that the superbill identifies this person and the actual family or group service. Do not change the code unless your record shows that a correction is required."
