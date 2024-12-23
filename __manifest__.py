# -*- coding:utf-8 -*-
############################################################################
#    Module Writen to OpenERP, Open Source Management Solution             #
#    Copyright (C) BIG Outsourcing (<http://www.bigoutsourcing.com.co>).   #
#    All Rights Reserved                                                   #
###############Credits######################################################
#    Coded by: Milet Johana Ruiz Lozano  desarrollo@masterquimica.com      #
#              Juan Carlos Barrero jbarrero@bigoutsourcing.com.co          #
#    Planified by: Juan Carlos Barrero                                     #
#    Finance by: BIG Outsourcing  http://www.bigoutsourcing.com.co         #
#    Audited by: Juan Carlos Barrero jbarrero@bigoutsourcing.com.co        #
############################################################################
#    This program is free software: you can redistribute it and/or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation, either version 3 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>. #
############################################################################

{
	'name' : 'BOS IT_Managment',
	'version' : '15.0.0.0',
    'sequence': 1 ,
	'author' : 'Milet Johana Ruiz Lozano',
    'company' : 'BIG Outsourcing S.A.S.',
    'website' : 'https://www.bigoutsourcing.com.co/',
    'category': 'website',
	'description' : "Basic example of a custom module",
	'depends' : [
        "base", "account", "hr", "helpdesk",
    	],
	'data' : [
        #security
        'security/it_mng_security.xml',
        'security/ir.model.access.csv',
        #data
        'data/hardware_type_data.xml',
        'data/record_type_data.xml',
        #views
        'views/it_mng.xml',
        #reports
        'reports/it_hardware_report.xml',

	],
	'installable' : True,
	'application' : False,
	'auto_install': False,
}