# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [0.1.1](https://github.com/vst/pypara/compare/0.1.0...0.1.1) (2023-10-11)


### Features

* add DateRange.endpoints property ([a346121](https://github.com/vst/pypara/commit/a346121fcb9a82c31f9388f8667b4963628b973f))

## [0.1.0](https://github.com/vst/pypara/compare/0.0.27...0.1.0) (2023-06-15)


### ⚠ BREAKING CHANGES

* drop Python 3.8 support
* drop {Money,Price}.{ccy,qty,dov} type hints
* make {Money,Price}.NA a classmethod, rename to .na

### Features

* add {Money,Price}.ccy_or_none method ([a6c25d1](https://github.com/vst/pypara/commit/a6c25d153288e5b66391bb694120b77de6942fb6))
* add {Money,Price}.dimap method ([0f10309](https://github.com/vst/pypara/commit/0f10309287995d8c68d76d075278b2d6f7a1552a))
* add {Money,Price}.dov_or_none method ([0ee64ab](https://github.com/vst/pypara/commit/0ee64ab44591c72ab8ca36a9b86796bc10134f03))
* add {Money,Price}.fmap method ([cffe534](https://github.com/vst/pypara/commit/cffe534eb91c2f86b688d9330800baac0b274879))
* add {Money,Price}.or_else method ([d7085cb](https://github.com/vst/pypara/commit/d7085cb52336a7037000234946882ce796cf7c11))
* add {Money,Price}.qty_map method ([f859908](https://github.com/vst/pypara/commit/f85990830e9fc47a87433840dd87c22ca98f1807))
* add {Money,Price}.qty_or_else method ([081b335](https://github.com/vst/pypara/commit/081b335c464dfa1cd413b05b66036bb0e40ea426))
* add {Money,Price}.qty_or_none method ([ae9c480](https://github.com/vst/pypara/commit/ae9c480d946a0a037bd3efe43c3b583019999d01))
* add {Money,Price}.qty_or_zero method ([62b97d4](https://github.com/vst/pypara/commit/62b97d4e1655f8cdb60504c27593e188cba81583))
* add type guards for {None,Some}{Money,Price} type checks ([98f8259](https://github.com/vst/pypara/commit/98f82596de8c07f7f071934a55dc083f1c942d53))


### Bug Fixes

* correct spelling for some documentation and exception messages ([a029cb8](https://github.com/vst/pypara/commit/a029cb8a567e3eaf482232a60e14f739bc73c961))
* drop Python 3.8 support ([c978c2e](https://github.com/vst/pypara/commit/c978c2e8e59e5a2d5d48612cd12fd1a57160a11b))
* fix Protocol definitions ([7977dd4](https://github.com/vst/pypara/commit/7977dd4bc9be32aae098941b376a3aae7c4c5c9a))
* make NonePrice.money a property ([a705315](https://github.com/vst/pypara/commit/a70531509acf3acd1fc92be3c036f9bf5ffa6231))
* use more common names for pre-defined currencies ([a00a403](https://github.com/vst/pypara/commit/a00a403af44ee0e053ec0d893cf6bc28079475aa))


### Code Refactoring

* drop {Money,Price}.{ccy,qty,dov} type hints ([c98b60d](https://github.com/vst/pypara/commit/c98b60d94717826635f5815b3f0205128f174337))
* make {Money,Price}.NA a classmethod, rename to .na ([c79b092](https://github.com/vst/pypara/commit/c79b092d535b721d95b1203225a0dab2b135e73f))


### Documentation

* update README ([74c76bc](https://github.com/vst/pypara/commit/74c76bc5b0282e739956816bfad8aa8ed7a09159))

## [0.0.27](https://github.com/vst/pypara/compare/0.0.26...0.0.27) (2023-06-13)


### Bug Fixes

* fix typo in currency type label ([200efb6](https://github.com/vst/pypara/commit/200efb66cbf5179d4e2b31b279b9d8b0d50236c7))


### Documentation

* revisit auto-generated documentation ([47f494c](https://github.com/vst/pypara/commit/47f494c65ff623c06178c64cdb379f70c2d373f3))
* update README ([cecf630](https://github.com/vst/pypara/commit/cecf6303dd76c25f50b0e5979f5671ad66a49b92))

### [0.0.26](https://github.com/vst/pypara/compare/0.0.25...0.0.26) (2021-05-06)


### Features

* add DOGE (dogecoin) to currency list ([9063ac7](https://github.com/vst/pypara/commit/9063ac7dbe085a28eebadcdcbf45ecc4d9dc7637))
* add XLC (ethereum lite cash) to currency list ([d46e3c6](https://github.com/vst/pypara/commit/d46e3c639936638bc2048ae3c2adb9b0ad9aed85))

### [0.0.25](https://github.com/vst/pypara/compare/0.0.24...0.0.25) (2021-04-22)


### Features

* add {ccy,qty,dov}_or methods to Money and Price ([9b1275b](https://github.com/vst/pypara/commit/9b1275bec2a0dd659d6179002b4f32bddc53c73b))

### [0.0.24](https://github.com/vst/pypara/compare/0.0.23...0.0.24) (2021-04-04)

### [0.0.23](https://github.com/vst/pypara/compare/0.0.22...0.0.23) (2021-04-04)


### Features

* **currency:** add new cryptocurrency LINK ([52e8ba7](https://github.com/vst/pypara/commit/52e8ba797f39e93605512a096420946740aa3989))

### [0.0.22](https://github.com/vst/pypara/compare/0.0.21...0.0.22) (2020-03-16)


### Bug Fixes

* enable ordering on `Currency` instances ([b9e08ca](https://github.com/vst/pypara/commit/b9e08cac244b4a7c50b7e359c0123a0cc24a1232))

### [0.0.21](https://github.com/vst/pypara/compare/0.0.20...0.0.21) (2020-03-16)


### Bug Fixes

* add missing .commons package ([d851cc8](https://github.com/vst/pypara/commit/d851cc8f65108daacff59f0ba7df7ab03f988c81))

### [0.0.20](https://github.com/vst/pypara/compare/0.0.19...0.0.20) (2020-03-16)
