<?php

define('ASVS_V2_JSON_FILE', realpath(__DIR__ . '/../src/asvs.json'));
define('ASVS_v3_JSON_FILE', realpath(__DIR__ . '/../src/asvs_v3.json'));

$v2 = json_decode(file_get_contents(ASVS_V2_JSON_FILE));
$v3 = json_decode(file_get_contents(ASVS_v3_JSON_FILE));

foreach ($v2->requirements as $v2Requirement) {
  // Invariant: each requirement must have an english title.
  if (!isset($v2Requirement->title->en)) {
    print 'Missing English text for:';
    var_dump($v2Requirement);
    exit(1);
  }

  $englishText = $v2Requirement->title->en;

  // Search through all v3 requirements for the same english text,
  // if found, copy over the other titles.
  foreach ($v3->requirements as $v3Requirement) {
    if ($v3Requirement->title->en === $englishText) {
      $v3Requirement->title = $v2Requirement->title;
    }
  }
}

file_put_contents(
  ASVS_v3_JSON_FILE,
  json_encode(
    $v3,
    JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES
  )
);

print ASVS_v3_JSON_FILE . ' updated' . PHP_EOL;
exit(0);
