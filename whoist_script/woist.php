<?php

// Read config file
if(!file_exists(getenv('HOME') . '/.woistdb')) {
	$config = array('known' => array());
} else {
	$config = json_decode(file_get_contents(getenv('HOME') . '/.woistdb'), true);
}


if($argc == 1) {
	echo 'Syntax: ' . $argv[0] . ' show' . PHP_EOL;
	echo 'Syntax: ' . $argv[0] . ' all' . PHP_EOL;
	echo 'Syntax: ' . $argv[0] . ' add <login> [nickname]' . PHP_EOL;
	echo 'Syntax: ' . $argv[0] . ' del <login>' . PHP_EOL;
	echo 'Syntax: ' . $argv[0] . ' list' . PHP_EOL;
	exit(-1);
}


$mode = $argv[1];

function write_config($config) {
	// Write config file
	$fp = fopen(getenv('HOME') . '/.woistdb', 'w+');
	if(!flock($fp, LOCK_EX)) {
		echo 'Could not get file lock.';
		exit(-1);
	}
	fwrite($fp, json_encode($config));
	fclose($fp);
}


// Add new user to database
if($mode == 'add') {
	if($argc != 3 && $argc != 4) {
		echo 'Invalid number of arguments.';
		exit(-1);
	}

	$login = $argv[2];
	$nickname = null;
	if($argc == 4) {
		$nickname = $argv[3];
	}

	$config['known'][$login] = $nickname;

	write_config($config);
	exit(0);
}


// Remove user from database
if($mode == 'del') {
	if($argc != 3) {
		echo 'Invalid number of arguments.';
		exit(-1);
	}
	$login = $argv[2];

	unset($config['known'][$login]);

	write_config($config);
	exit(0);
}


// Show database
if($mode == 'list') {
	if($argc != 2) {
		echo 'Invalid number of arguments.';
		exit(-1);
	}

	echo 'Database:' . PHP_EOL;
	foreach($config['known'] as $login => $nickname) {
		echo '- ' . $login . ': ' . $nickname . PHP_EOL;
	}

	exit(0);
}





function hostmatch($h, $p) {
	if(preg_match('/^' . $p . '$/', $h)) return true;
	return false;
}

function getCip($host) {

	if(hostmatch($host, 'faui03i')
	) return 'FSI-Zimmer';

	if(hostmatch($host, 'faui00[a-y]')
	|| hostmatch($host, 'faui02[a-y]')
	|| hostmatch($host, 'faui0f[a-u]')
	) return 'Cip 2';

	if(hostmatch($host, 'faui0a[a-q]')
	|| hostmatch($host, 'faui0b[a-l]')
	) return 'BibCip';

	if(hostmatch($host, 'faui0e[a-o]')
	|| hostmatch($host, 'faui06[a-q]')
	|| hostmatch($host, 'faui05[a-h]')
	|| hostmatch($host, 'faui08[a-p]')
	) return 'Cip 1';

	if(hostmatch($host, 'faui09[a-j]')
	|| hostmatch($host, 'faui01[a-r]')
	) return 'WinCip';

	if(hostmatch($host, 'faui0d[a-u]')
	) return 'STFUcip';

	if(hostmatch($host, 'faui0c[a-q]')
	) return 'CIP4';

	if(hostmatch($host, 'faui04[a-s]')
	) return 'Huber-Cip';

	return 'unknown';
}

function mkspace($num) {
	$res = '';
	for($i = 0; $i < $num; $i++) {
		$res .= ' ';
	}
	return $res;
}


if($mode == 'show' || $mode == 'all') {

	$showall = false;
	if($mode == 'all') $showall = true;


	$result = array();

	$current_hostname = '';
	$rows = file('/proj/ciptmp/av37umic/scripts/woist.txt');
	if(!$rows) {
		echo 'Error reading list.';
		exit(-1);
	}

	foreach($rows as $r) {
		if(preg_match('/^(faui0..)\./', $r, $matches)) {
			$current_hostname = $matches[1];
			continue;
		}

		if($r) {
			preg_match('/^([^ ]+) \(([^,]+).+? (\d+)$/', $r, $matches);
			if(!$matches) continue;

			$login = $matches[1];
			$name = $matches[2];
			$idletime = $matches[3];

			if(!$showall && !array_key_exists($login, $config['known'])) continue;

			if($idletime < 900) {
				$prefix = "\t";
				$nickname = '';
				if(array_key_exists($login, $config['known'])) {
					$nickname = $config['known'][$login];
					if($showall) {
						$prefix = '     *  ';
					}
				}
				$result[getCip($current_hostname)][] = $prefix . $login . mkspace(12 - strlen($login)) . $nickname . mkspace(15 - strlen($nickname)) . $name . mkspace(30 - strlen($name)) . ' (' . $current_hostname . ')';
			}
		}
	}


	foreach($result as $cip => $a) {
		echo $cip . PHP_EOL;
		foreach($a as $r) {
			echo $r . PHP_EOL;
		}
	}

	exit(0);
}

echo 'Invalid mode!';
exit(-1);

