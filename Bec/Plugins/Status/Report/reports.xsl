<!-- This file is only provided as a example. and needs to be edited to sute your style. -->

<?xml version='1.0'?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
    <body style="background:#444444; color:#ffffff;">
      
		<center>
			<div style = "width:580px; background:#000000; color:#ffffff; margin:50 auto">
			
				<hr style='margin-top:50px'/>
				<div style="text-align:center"><xsl:value-of select="BecStatus/hostname"/></div>
				<hr style='margin-top:0px'/>
			
				<div style="text-align:left; padding-left:5px">
					<span>Bec Version: <xsl:value-of select="BecStatus/becversion"/>, </span>
					<span>Be Version: <xsl:value-of select="BecStatus/beversion"/>, </span>
					<span>Server Version: <xsl:value-of select="BecStatus/gamever"/>, </span>
					<span>Bec Reporter: <xsl:value-of select="BecStatus/becreporter"/></span>
				</div>
		
				<div style="text-align:left; padding-left:5px">
					<span>Last updated: <xsl:value-of select="BecStatus/lastupdate"/>, </span>
					<span>Next updated: <xsl:value-of select="BecStatus/nextupdate"/> </span>
				</div>

				<div style="text-align:left; padding-left:5px">
					<span>Bec Uptime: <xsl:value-of select="BecStatus/becuptime"/>, </span>
					<span>Server Uptime: <xsl:value-of select="BecStatus/serveruptime"/></span>
				</div>		
				
				
				<hr style='margin-top:0px;'/>
				<div style='margin-top:-10px;'>
					<div title="Number of admins online" style='width:65px; display:inline-block'>Ao: <xsl:value-of select="BecStatus/numadmins"/></div>
					<div title="Number of temp admins online" style=' width:65px;display:inline-block'>Tao: <xsl:value-of select="BecStatus/numtmpadmins"/></div>	
					<div title="Number of kicks this Bec session" style='width:65px;display:inline-block'>Kts: <xsl:value-of select="BecStatus/kts"/></div>
					<div title="Number of bans this Bec session" style='width:65px;display:inline-block'>Bts: <xsl:value-of select="BecStatus/bts"/></div>
					<div title="Number of hacks this Bec session"  style='width:65px;display:inline-block'>Hts: <xsl:value-of select="BecStatus/hts"/></div>
					<div title="Number of connections this Bec session" style='width:65px;display:inline-block'>Cts: <xsl:value-of select="BecStatus/cts"/></div>
					<div title="Number of  uniqe connections this Bec session" style='width:65px;display:inline-block'>Uts: <xsl:value-of select="BecStatus/uts"/></div>
				</div>
				
				<hr style='margin-top:0px;'/>				
			
				<div style="margin-top:-8px; text-align:left; padding-left:5px">
					<span>Players: <xsl:value-of select="BecStatus/numplayers"/>, </span>
					<span>Map: <xsl:value-of select="BecStatus/mapname"/>, </span>
					<span>Mission: <xsl:value-of select="BecStatus/mission"/>, </span>
					<span>Gametype: <xsl:value-of select="BecStatus/gametype"/>, </span>
					<span>Difficulty: <xsl:value-of select="BecStatus/difficulty"/></span>
				</div>			
				
				<hr style='margin-top:0px'/>
				<xsl:choose>
					<xsl:when test="BecStatus/players/player">
						<table border="0" style="width:560px; text-align:center">
							<xsl:for-each select="BecStatus/players/player">
								<xsl:if test="(position() mod 4) = 1">
									<tr>
										<td><xsl:value-of select="."/></td>
										<td><xsl:value-of select="following-sibling::player[position()=1]"/></td>
										<td><xsl:value-of select="following-sibling::player[position()=2]"/></td>
										<td><xsl:value-of select="following-sibling::player[position()=3]"/></td>
									</tr>
								</xsl:if>
							</xsl:for-each>
						</table>
					</xsl:when>
					<xsl:otherwise>
					Waiting for players..
					</xsl:otherwise>
				</xsl:choose>
			  <hr style='margin-top:4px'/>
			</div>
		</center>
    </body>
  </html>
</xsl:template>

</xsl:stylesheet>