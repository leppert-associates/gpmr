SELECT
a.cas, a.analytename,
d.dataresults, d.qualifiers, d.dataresultsunitstypeluid,
c.fieldsamplenameassignment,
l.locationarrivaldatetime
FROM ((("1".samplelabdata d
    LEFT OUTER JOIN "0".analyte a
        ON a.analyteid = d.analyteid)
    LEFT OUTER JOIN "1".samplecontainer c
        ON c.samplecontainerid = d.samplecontainerid)
    LEFT OUTER JOIN "1".sampledatacollect l
        ON l.sampledatacollectid = c.sampledatacollectid)
LIMIT 25