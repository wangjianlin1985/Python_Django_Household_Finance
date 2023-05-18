/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50620
Source Host           : localhost:3306
Source Database       : family_cash_db

Target Server Type    : MYSQL
Target Server Version : 50620
File Encoding         : 65001

Date: 2019-09-20 16:30:57
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `t_admin`
-- ----------------------------
DROP TABLE IF EXISTS `t_admin`;
CREATE TABLE `t_admin` (
  `username` varchar(20) NOT NULL DEFAULT '',
  `password` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_admin
-- ----------------------------
INSERT INTO `t_admin` VALUES ('a', 'a');

-- ----------------------------
-- Table structure for `t_expend`
-- ----------------------------
DROP TABLE IF EXISTS `t_expend`;
CREATE TABLE `t_expend` (
  `expendId` int(11) NOT NULL AUTO_INCREMENT COMMENT '支出id',
  `exprendTypeObj` int(11) NOT NULL COMMENT '支出类型',
  `expendPurpose` varchar(60) NOT NULL COMMENT '支出用途',
  `payWayObj` int(11) NOT NULL COMMENT '支付方式',
  `payAccount` varchar(20) NOT NULL COMMENT '支付账号',
  `expendMoney` float NOT NULL COMMENT '支付金额',
  `expendDate` varchar(20) DEFAULT NULL COMMENT '支付日期',
  `userObj` varchar(30) NOT NULL COMMENT '支出用户',
  `expendMemo` varchar(20) DEFAULT NULL COMMENT '支出备注',
  PRIMARY KEY (`expendId`),
  KEY `exprendTypeObj` (`exprendTypeObj`),
  KEY `payWayObj` (`payWayObj`),
  KEY `userObj` (`userObj`),
  CONSTRAINT `t_expend_ibfk_1` FOREIGN KEY (`exprendTypeObj`) REFERENCES `t_expendtype` (`expendTypeId`),
  CONSTRAINT `t_expend_ibfk_2` FOREIGN KEY (`payWayObj`) REFERENCES `t_payway` (`payWayId`),
  CONSTRAINT `t_expend_ibfk_3` FOREIGN KEY (`userObj`) REFERENCES `t_userinfo` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_expend
-- ----------------------------
INSERT INTO `t_expend` VALUES ('1', '1', '9月逛街买衣服', '1', 'wanggege@163.com', '350', '2019-09-20', 'father', '给老婆用的');
INSERT INTO `t_expend` VALUES ('2', '3', '手机充值话费', '2', 'mengxiaowei', '50', '2019-09-19', 'mother', '自己手机用');
INSERT INTO `t_expend` VALUES ('3', '2', '吃串串香', '3', '--', '98', '2019-09-19', 'mother', '和老公一起吃');

-- ----------------------------
-- Table structure for `t_expendtype`
-- ----------------------------
DROP TABLE IF EXISTS `t_expendtype`;
CREATE TABLE `t_expendtype` (
  `expendTypeId` int(11) NOT NULL AUTO_INCREMENT COMMENT '支出类型id',
  `expendTypeName` varchar(20) NOT NULL COMMENT '支出类型名称',
  PRIMARY KEY (`expendTypeId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_expendtype
-- ----------------------------
INSERT INTO `t_expendtype` VALUES ('1', '衣服');
INSERT INTO `t_expendtype` VALUES ('2', '餐饮');
INSERT INTO `t_expendtype` VALUES ('3', '电话费');

-- ----------------------------
-- Table structure for `t_income`
-- ----------------------------
DROP TABLE IF EXISTS `t_income`;
CREATE TABLE `t_income` (
  `incomeId` int(11) NOT NULL AUTO_INCREMENT COMMENT '收入id',
  `incomeTypeObj` int(11) NOT NULL COMMENT '收入类型',
  `incomeFrom` varchar(50) NOT NULL COMMENT '收入来源',
  `payWayObj` int(11) NOT NULL COMMENT '支付方式',
  `payAccount` varchar(20) NOT NULL COMMENT '支付账号',
  `incomeMoney` float NOT NULL COMMENT '收入金额',
  `incomeDate` varchar(20) DEFAULT NULL COMMENT '收入日期',
  `userObj` varchar(30) NOT NULL COMMENT '收入用户',
  `incomeMemo` varchar(800) DEFAULT NULL COMMENT '收入备注',
  PRIMARY KEY (`incomeId`),
  KEY `incomeTypeObj` (`incomeTypeObj`),
  KEY `payWayObj` (`payWayObj`),
  KEY `userObj` (`userObj`),
  CONSTRAINT `t_income_ibfk_1` FOREIGN KEY (`incomeTypeObj`) REFERENCES `t_incometype` (`typeId`),
  CONSTRAINT `t_income_ibfk_2` FOREIGN KEY (`payWayObj`) REFERENCES `t_payway` (`payWayId`),
  CONSTRAINT `t_income_ibfk_3` FOREIGN KEY (`userObj`) REFERENCES `t_userinfo` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_income
-- ----------------------------
INSERT INTO `t_income` VALUES ('1', '1', '9月份领取工资', '1', 'wanggege@163.com', '6200', '2019-09-20', 'father', 'test');
INSERT INTO `t_income` VALUES ('2', '2', '8月份全勤奖领取', '1', 'xiaowei@126.com', '350', '2019-09-12', 'mother', '我的奖金哦');
INSERT INTO `t_income` VALUES ('3', '1', '9月份发的工资', '1', 'xiaowei@126.com', '3850', '2019-09-20', 'mother', '我的工资啊');

-- ----------------------------
-- Table structure for `t_incometype`
-- ----------------------------
DROP TABLE IF EXISTS `t_incometype`;
CREATE TABLE `t_incometype` (
  `typeId` int(11) NOT NULL AUTO_INCREMENT COMMENT '分类id',
  `typeName` varchar(20) NOT NULL COMMENT '分类名称',
  PRIMARY KEY (`typeId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_incometype
-- ----------------------------
INSERT INTO `t_incometype` VALUES ('1', '工资');
INSERT INTO `t_incometype` VALUES ('2', '奖金');

-- ----------------------------
-- Table structure for `t_notice`
-- ----------------------------
DROP TABLE IF EXISTS `t_notice`;
CREATE TABLE `t_notice` (
  `noticeId` int(11) NOT NULL AUTO_INCREMENT COMMENT '公告id',
  `title` varchar(80) NOT NULL COMMENT '标题',
  `content` varchar(5000) NOT NULL COMMENT '公告内容',
  `publishDate` varchar(20) DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`noticeId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_notice
-- ----------------------------
INSERT INTO `t_notice` VALUES ('1', '家庭财务网站成立了', '<p>以后家里的所有收入和开支都归此系统管理哈！</p>', '2019-09-20 15:21:40');

-- ----------------------------
-- Table structure for `t_payway`
-- ----------------------------
DROP TABLE IF EXISTS `t_payway`;
CREATE TABLE `t_payway` (
  `payWayId` int(11) NOT NULL AUTO_INCREMENT COMMENT '支付方式id',
  `payWayName` varchar(20) NOT NULL COMMENT '支付方式名称',
  PRIMARY KEY (`payWayId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_payway
-- ----------------------------
INSERT INTO `t_payway` VALUES ('1', '支付宝');
INSERT INTO `t_payway` VALUES ('2', '微信');
INSERT INTO `t_payway` VALUES ('3', '现金');

-- ----------------------------
-- Table structure for `t_userinfo`
-- ----------------------------
DROP TABLE IF EXISTS `t_userinfo`;
CREATE TABLE `t_userinfo` (
  `user_name` varchar(30) NOT NULL COMMENT 'user_name',
  `password` varchar(30) NOT NULL COMMENT '登录密码',
  `name` varchar(20) NOT NULL COMMENT '姓名',
  `gender` varchar(4) NOT NULL COMMENT '性别',
  `birthDate` varchar(20) DEFAULT NULL COMMENT '出生日期',
  `userPhoto` varchar(60) NOT NULL COMMENT '用户照片',
  `telephone` varchar(20) NOT NULL COMMENT '联系电话',
  `email` varchar(50) NOT NULL COMMENT '邮箱',
  `address` varchar(80) DEFAULT NULL COMMENT '家庭地址',
  `regTime` varchar(20) DEFAULT NULL COMMENT '注册时间',
  PRIMARY KEY (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_userinfo
-- ----------------------------
INSERT INTO `t_userinfo` VALUES ('father', '123', '父亲汪大神', '男', '2019-09-11', 'img/father.jpg', '13890825934', 'wanglin@163.com', '四川成都市区', '2019-09-20 15:17:52');
INSERT INTO `t_userinfo` VALUES ('mother', '123', '母亲萌小薇', '女', '2019-09-11', 'img/12.jpg', '13980810834', 'xiaowei@126.com', '江西南昌', '2019-09-20 15:31:25');
