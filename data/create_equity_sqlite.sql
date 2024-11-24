CREATE TABLE [EquityDailyPrice](
	[Ticker] [nvarchar](50),
	[AsOfDate] [date],
	[Open] [float] NOT NULL,
	[High] [float] NOT NULL,
	[Low] [float] NOT NULL,
	[Close] [float] NOT NULL,
	[Volume] [float] NOT NULL,
	[Dividend] [float] NOT NULL,
	[StockSplits] [int] NOT NULL,	
	primary key (Ticker, AsOfDate)
 );

CREATE TABLE [ETFDailyPrice](
	[Ticker] [nvarchar](50),
	[AsOfDate] [date],
	[Open] [float] NOT NULL,
	[High] [float] NOT NULL,
	[Low] [float] NOT NULL,
	[Close] [float] NOT NULL,
	[Volume] [float] NOT NULL,
	[Dividend] [float] NOT NULL,
	[StockSplits] [int] NOT NULL,	
	primary key (Ticker, AsOfDate)
 );

CREATE TABLE [EquityTechnicalIndicators](
	[Ticker] [nvarchar](50),
	[AsOfDate] [date],
	[Close] [float] NOT NULL,
	[Volume] [float] NOT NULL,
	[SMA10] [float] NULL,
	[SMA20] [float] NULL,
	[SMA50] [float] NULL,
	[SMA200] [float] NULL,			
	[RSI] [float] NULL,
	[MACDline] [float] NULL,
	[MACDsignal] [float] NULL,
	[BBupperBand] [float] NULL,
	[BBmiddleBand] [float] NULL,
	[BBlowerBand] [float] NULL,
	[ADX] [float] NULL,
	[DMP] [float] NULL,
	[DMN] [float] NULL,
	primary key (Ticker, AsOfDate)
 );



CREATE TABLE [EquityIntradayPrice](
	[Ticker] [nvarchar](50) NOT NULL,
	[AsOfDate] [date] NOT NULL,
	[DateIndex] [int] NOT NULL,
	[AsOfTime] [datetime] NOT NULL,
	[Open] [float] NOT NULL,
	[High] [float] NOT NULL,
	[Low] [float] NOT NULL,
	[Close] [float] NOT NULL,
	[Volume] [float] NOT NULL,
	primary key (Ticker, AsOfTime)
);
