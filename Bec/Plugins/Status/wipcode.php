<?php

// Warning.. this is horrible php code. and only ment to be provided as a poc code.
// php is not my main language. ;)

$FILENAME = 'Bec_arma3_server.xml';		// SET CORRECT STATUS FILE NAME HERE 
$ServerIP = "127.0.0.1";				// SET CORRECT SERVER IP.. HERE
$ServerPort = 2320;						// SET CORRECT SERVER PORT HERE

// Load the document and get basic the data.
$doc = new DOMDocument();
$doc->load( $FILENAME );

$hostname		= $doc->getElementsByTagName("hostname")->item(0)->nodeValue;
$gamever		= $doc->getElementsByTagName("gamever")->item(0)->nodeValue;
$mapname		= $doc->getElementsByTagName("mapname")->item(0)->nodeValue;
$mission		= $doc->getElementsByTagName("mission")->item(0)->nodeValue;
$gametype		= $doc->getElementsByTagName("gametype")->item(0)->nodeValue;
$numplayers		= $doc->getElementsByTagName("numplayers")->item(0)->nodeValue;
$lastupdate		= $doc->getElementsByTagName("lastupdate")->item(0)->nodeValue;
$becversion		= $doc->getElementsByTagName("becversion")->item(0)->nodeValue;
$becuptime		= $doc->getElementsByTagName("becuptime")->item(0)->nodeValue;
$becreporter	= (($doc->getElementsByTagName("becreporter")->item(0)->nodeValue) == "1") ? "Yes" : "No";
$serveruptime	= $doc->getElementsByTagName("serveruptime")->item(0)->nodeValue;

$kts			= $doc->getElementsByTagName("kts")->item(0)->nodeValue;
$bts			= $doc->getElementsByTagName("bts")->item(0)->nodeValue;
$hts			= $doc->getElementsByTagName("hts")->item(0)->nodeValue;
$cts			= $doc->getElementsByTagName("cts")->item(0)->nodeValue;
$uts			= $doc->getElementsByTagName("uts")->item(0)->nodeValue;
$numadmins		= $doc->getElementsByTagName("numadmins")->item(0)->nodeValue;
$numtmpadmins	= $doc->getElementsByTagName("numtmpadmins")->item(0)->nodeValue;

$playerlist = array();
$players= $doc->getElementsByTagName("player");
foreach ($players as $player ) {$playerlist[] = $player->nodeValue;};

echo "<style type='text/css'>
div.main {
	width:530px;
	background:#000000;
	color:#ffffff;
	margin:50 auto;
}


#general {
	text-align:left; 
	background:#000000;
	color:#ffffff;
	padding-left:6px;
	padding-top:0px;
	font-family:Arial;	
	font-size : 11px;
}

#players {
	width:530px;
	background:#000000;
	color:#ffffff;
	padding-left:3px;
	padding-top:0px;
	font-family:Arial;	
	font-size : 10px;
	margin-top:-6px;	
	margin-bottom:0px;	
}


#topframe {
	height:22px; 
	width:530px; 
	background:#44aacc;
	font-family:times;
	font-size : 16px;
	font-family:georgian;	
	font-weight:bold;
	text-shadow: 1px 1px 0px #000000;
}
#steamlink {
	text-decoration : none;
	color:#eeeeee;
	margin-top:-15px;	
}

</style>";

$html = "
<div class='main'>

	<div id='topframe' title='Start steam and join the server'>
		<div style='display:inline-block;margin-top:2px;'>
			<img src = 'http://127.0.0.1/becstatus/img/clan_logo.ico' style='height:16px;padding-left:2px;vertical-align:text-top;'/>
		</div>
		<div style='display:inline-block;margin-top:-2px;'>
			<a id='steamlink' href='steam://rungameid/107410//-connect=$ServerIP -port=$ServerPort -skipintro -nosplash'>".$hostname."</a>
		</div>
	</div>
	<hr style='margin-top:-2px'/>
	<div id='general'  style='margin-top:-8px'>
		<div style='display:inline-block'>Bec Version: ".$becversion."</div>
		<div style='display:inline-block; width:310px'>, Server Version: ".$gamever."</div>
		<div style='display:inline-block; text-align:left; width:100px; margin-left:-2px'>Bec Reporter: ".$becreporter."</div>
	</div>

	<div id='general' >
		<div style='display:inline-block; width:398px;'>Status last updated: ".$lastupdate."</div>
		<div style='display:inline-block'>Players (".$numplayers.")</div>
	</div>

	<div id='general'>
		<span>Bec uptime: ".$becuptime."</span>
		<span>, Server uptime: ".$serveruptime."</span>
	</div>
	<div id='general'>
		<span>Map: ".$mapname."</span>
		<span>, Mission: ".$mission."</span>
		<span>, Gametype: ".$gametype."</span>
	</div>	
	
	<hr style='margin-top:0px;'/>
	<div style='margin-top:-12px;'>
	<div id='general' style='width:65px; display:inline-block'>Ao: ".$numadmins."</div>
	<div id='general' style=' width:65px;display:inline-block'>To: ".$numtmpadmins."</div>	
	<div id='general' style='width:65px;display:inline-block'>Kts: ".$kts."</div>
	<div id='general' style='width:65px;display:inline-block'>Bts: ".$bts."</div>
	<div id='general' style='width:65px;display:inline-block'>Hts: ".$hts."</div>
	<div id='general' style='width:65px;display:inline-block'>Cts: ".$cts."</div>
	<div id='general' style='width:65px;display:inline-block'>Uts: ".$uts."</div>
	</div>
	<hr style='margin-top:-2px;'/>";
	
	$html_table = '<table id="players"><tr>';
	$col_size = 6;

	if ($numplayers > 0) {
		for($i=0; $i<count($playerlist); $i++) {
			$html_table .= '<td style="background:#000000;margin-top:0px;height:11px"><div title="'.$playerlist[$i].'"style="margin-top:-5px;width:75px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;">' .$playerlist[$i]. '</div></td>';   	
			if(($i+1) % $col_size == 0) { $html_table .= '</tr><tr >'; }
		}
	}
	$html_table .= '</tr></table>'; 
	$html_table = str_replace('<tr></tr>', '', $html_table);

$html = $html . $html_table . "</div>";
echo $html;
?>